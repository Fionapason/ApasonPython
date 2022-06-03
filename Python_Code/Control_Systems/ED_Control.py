import time

from Sensor_Instrument_Tracking import Sensor_Update_List as ul
from Configurations import Configurations_Control_Systems as conf

"""
Here the ED-specific sub-control systems are implemented as classes, as well as the EDs general control system.

The ED_Massflow_PI class uses a Proportional-Integral controller to maintain a steady massflow from all four of its pumps.
The PI controller checks the current massflow and, using experimentally determined K_p and K_i parameters,
adjusts the voltage set at the DAC output, which determines the pump force.

The ED_Conductivity_Pi class uses a similar controller to set the desired massflow of the diluate and concentrate stream,
dependent on the conductivity of the diluate output. If the diluate out conductivity is too high, this means that the
residence time within the electro-dialysis unit is not long enough and the massflow must be reduced accordingly.
Otherwise, we can try to maximize our output by pushing the diluate and concentrate flows to their limits, while
maintaining the water quality we want.

The ED_Pressure_Control class ensures that certain pressure differences that fall over different parts of the ED module
are maintained.

The ED class effectively runs the ED, taking instances of the aforementioned classes members, as well as controlling tank levels
and taking care of filling the concentrate tank.
"""

class ED_Massflow_PI:
    K_p : float
    K_i : float
    desired_value : float
    integral : float
    non_saturated_output : float
    pump_output : float # in Volt!

    first_loop = True

    control_value_sensor_name : str # Massflow sensor
    control_instrument_name : str # Pump

    def __init__(self, update_list, apason_system, control_configuration : str):

        self.K_p = conf.control_configurations[control_configuration]["K_p"]
        self.K_i = conf.control_configurations[control_configuration]["K_i"]
        self.desired_value = conf.control_configurations[control_configuration]["desired_value"]
        self.integral = 0.0
        self.pump_output = 0.0
        self.non_saturated_output = 0.0
        self.system_time_start = apason_system.time_start
        self.adjustment = 1.0

        self.control_value_sensor_normal_name = conf.control_configurations[control_configuration]["control_value_sensor_normal_name"]
        self.control_value_sensor_reversal_name = conf.control_configurations[control_configuration]["control_value_sensor_reversal_name"]

        self.control_instrument_name = conf.control_configurations[control_configuration]["control_instrument_name"]

        self.pressure_dependent = conf.control_configurations[control_configuration]["pressure_dependent"]

        # iterate through the update list to find the sensors we want to keep track of in either of our modes
        for sensor in update_list.massflow:
            if sensor.name == self.control_value_sensor_normal_name:
                self.control_value_sensor_normal: ul.Update_List_Massflow = sensor
            if sensor.name == self.control_value_sensor_reversal_name:
                self.control_value_sensor_reversal : ul.Update_List_Massflow = sensor

        # iterate through apason system to find the instrument we want to be able to adjust
        for instrument in apason_system.system_pumps:
            if instrument.name == self.control_instrument_name:
                self.control_instrument = instrument
                break

        # start in normal mode
        self.control_value_sensor = self.control_value_sensor_normal


    def set_reversal_control(self):
        # in reversal, the PT, diluate and concentrate pumps are all working to maintain the diluate flow
        self.control_value_sensor = self.control_value_sensor_reversal
        self.reset_pump_control()

    def set_normal_control(self):
        self.control_value_sensor = self.control_value_sensor_normal
        self.reset_pump_control()

    def stop_pump(self):
        self.control_instrument.set_new_state(0.0)
        print(self.control_instrument_name + " SET TO 0.")

    def reset_pump_control(self):
        print("RESETTING " + self.control_instrument_name)
        # PI control needs to start anew, so we reset all values relevant to that
        self.integral = 0.0
        self.pump_output = 0.0  # in Volt!
        self.non_saturated_output = 0.0
        self.system_time_start = time.time()
        self.first_loop = True

    def massflow_pi(self):

        print("---------- \n Desired Massflow for "  + self.control_instrument_name + ": " + str(self.desired_value))

        if self.first_loop:
            self.time_start = time.time()  # current time in seconds
            self.time_current = self.time_start
            self.time_last = self.time_current
            elapsed_time = self.time_start - self.system_time_start
            self.first_loop = False
        else:
            self.time_current = time.time()
            elapsed_time = self.time_current - self.time_last

        sensor = self.control_value_sensor
        last_measurement = sensor.current_value
        error = self.desired_value - last_measurement

        # to ensure the PI controller doesn't happen too often, we make sure at least one second has passed
        if elapsed_time > 1.0:
            # Proportional Controller
            P_out = self.K_p * error

            # Integrative Controller
            if self.non_saturated_output is not self.pump_output:
                I_out = 0.0
            else:
                self.integral = self.integral + elapsed_time * error
                I_out = self.K_i * self.integral

            out = P_out + I_out

            # control adder
            self.pump_output = self.pump_output + out

            # Do this before possible saturation
            self.non_saturated_output = self.pump_output

            # make sure we aren't already at the maximum or below 0: saturation check
            if self.pump_output > 5.0:
                self.pump_output = 5.0
            elif self.pump_output < 0.0:
                self.pump_output = 0.0

            self.pump_output = self.pump_output

            print("Setting " + self.control_instrument_name + " to Voltage: " + str(self.pump_output) + "\n----------")

            # the pressure control can adjust the output voltage slightly, to maintain a small pressure difference between streams
            if self.pressure_dependent:
                self.control_instrument.set_new_state(self.control_instrument.voltage_to_rpm(self.pump_output * self.adjustment))
            else:
                self.control_instrument.set_new_state(self.control_instrument.voltage_to_rpm(self.pump_output))

            self.time_last = self.time_current


class ED_Conductivity_PI:

    def __init__(self, update_list, apason_system, control_configuration : str,
                 ed_concentrate_flow_control  : ED_Massflow_PI, ed_diluate_flow_control  : ED_Massflow_PI, ed_pt_flow_control  : ED_Massflow_PI):

        self.K_p = conf.control_configurations[control_configuration]["K_p"]
        self.K_i = conf.control_configurations[control_configuration]["K_i"]
        self.desired_value = conf.control_configurations[control_configuration]["desired_value"]
        self.integral = 0.0
        self.massflow_set_value_output = 0.0
        self.non_saturated_output = 0.0
        self.system_time_start = apason_system.time_start

        self.control_value_sensor_name = conf.control_configurations[control_configuration]["conductivity_sensor_name"]
        self.control_cv3_name = conf.control_configurations[control_configuration]["control_cv3"]


        self.minimum_flow = conf.control_configurations[control_configuration]["minimum_flow"]
        self.maximum_flow = conf.control_configurations[control_configuration]["maximum_flow"]

        # so we can access the relevant flows directly
        self.concentrate_flow = ed_concentrate_flow_control
        self.diluate_flow = ed_diluate_flow_control
        self.posttreatment_flow = ed_pt_flow_control

        self.desired_flow = conf.control_configurations[control_configuration]["minimum_flow"]


        for sensor in update_list.conductivity:
            if sensor.name == self.control_value_sensor_name:
                self.control_value_sensor: ul.Update_List_Conductivity= sensor
                break
        for cv3 in apason_system.system_cv3s:
            if cv3.name == self.control_cv3_name:
                self.control_cv3 =  cv3
                break

        self.first_loop = True


    def conductivity_pi(self):

        if self.first_loop:
            self.time_start = time.time()  # current time in seconds
            self.time_current = self.time_start
            self.time_last = self.time_current
            elapsed_time = self.time_start - self.system_time_start
            self.first_loop = False
        else:
            self.time_current = time.time()
            elapsed_time = self.time_current - self.time_last

        sensor = self.control_value_sensor
        last_measurement = sensor.current_value
        error = self.desired_value - last_measurement

        if (last_measurement > 1) & (self.control_cv3.state == "LOW"):
            self.control_cv3.set_new_state("HIGH")
        elif (last_measurement < 1) & (self.control_cv3.state == "HIGH"):
            self.control_cv3.set_new_state("LOW")

        # Conductivity control should be slower than massflow control, so we only do it every 10 seconds
        if elapsed_time > 10.0:
            # Proportional Controller
            P_out = self.K_p * error

            # Integrative Controller
            if self.non_saturated_output is not self.massflow_set_value_output:
                I_out = 0.0
            else:
                self.integral = self.integral + elapsed_time * error
                I_out = self.K_i * self.integral
            out = P_out + I_out

            # control adder
            self.massflow_set_value_output = self.massflow_set_value_output + out

            # Do this before possible saturation
            self.non_saturated_output = self.massflow_set_value_output

            # make sure we aren't already at the maximum or below 0: saturation check
            if self.massflow_set_value_output > self.maximum_flow:
                self.massflow_set_value_output = self.maximum_flow
            elif self.massflow_set_value_output < self.minimum_flow:
                self.massflow_set_value_output = self.minimum_flow

            print("------------- \n Setting desired massflow to: " + str(self.massflow_set_value_output) + "\n ------------")

            self.desired_flow = self.massflow_set_value_output

            self.new_desired_flows(self.massflow_set_value_output)

            self.time_last = self.time_current



    def new_desired_flows(self, desired_flow):
        self.concentrate_flow.desired_value = desired_flow
        self.diluate_flow.desired_value = desired_flow
        self.posttreatment_flow.desired_value = desired_flow


class ED_Pressure_Control:

    def __init__(self, update_list, ed_massflow_diluate, ed_massflow_concentrate):

        self.critical_value_dc = conf.control_configurations["ed_pressures"]["critical_value_DC"]
        self.critical_value_rd = conf.control_configurations["ed_pressures"]["critical_value_RD"]

        self.concentrate_pressure_sensor_name = conf.control_configurations["ed_pressures"]["concentrate_pressure_sensor_name"]
        self.rinse_pressure_sensor_name = conf.control_configurations["ed_pressures"]["rinse_pressure_sensor_name"]
        self.diluate_pressure_sensor_name = conf.control_configurations["ed_pressures"]["diluate_pressure_sensor_name"]

        for sensor in update_list.pressure:
            if sensor.name == self.concentrate_pressure_sensor_name:
                self.concentrate_pressure_sensor: ul.Update_List_Pressure = sensor
            elif sensor.name == self.rinse_pressure_sensor_name:
                self.rinse_pressure_sensor: ul.Update_List_Pressure = sensor
            elif sensor.name == self.diluate_pressure_sensor_name:
                self.diluate_pressure_sensor: ul.Update_List_Pressure = sensor

        self.ed_massflow_diluate : ED_Massflow_PI = ed_massflow_diluate
        self.ed_massflow_concentrate : ED_Massflow_PI = ed_massflow_concentrate


        self.pdrd_problem = False
        self.pddc_problem = False

        self.pddc_potential_problem = False


    def current_concentrate_diluate_pressure_difference(self):
        concentrate_pressure = self.concentrate_pressure_sensor.current_value
        diluate_pressure = self.diluate_pressure_sensor.current_value
        pddc = diluate_pressure - concentrate_pressure
        print("CURRENT PDDC: " + str(pddc) + "\n")
        return pddc

    def pddc_exceeded(self):
        return abs(self.current_concentrate_diluate_pressure_difference()) > self.critical_value_dc

    def pddc_exceeded_positive_sign(self):
        return self.current_concentrate_diluate_pressure_difference() > 0

    def current_diluate_rinse_pressure_difference(self):
        rinse_pressure = self.rinse_pressure_sensor.current_value
        diluate_pressure = self.diluate_pressure_sensor.current_value
        pdrd = diluate_pressure - rinse_pressure
        print("CURRENT PDRD: " + str(pdrd) + "\n")
        return pdrd

    def pddc_large_time(self):

        # If the maximum Diluate-Concentrate difference has been reached, we can try to lower it by slightly
        # However, if too much time passes, we should shut the system off.

        pddc = self.current_concentrate_diluate_pressure_difference()

        if (abs(pddc) > 0.2) & (not self.pddc_potential_problem):
            self.pddc_problem_start_time = time.time()
            self.pddc_potential_problem = True
            print("THE PDDC JUST EXCEEDED 0.2. TRYING TO ADJUST. \n")

        elif (abs(pddc) > 0.2) & (self.pddc_potential_problem):
            if time.time() - self.pddc_problem_start_time > 30.0:
                self.pddc_problem = True
            else:
                print("STILL STABILIZING. " + str(time.time() - self.pddc_problem_start_time) + " SECONDS PASSED.")


    def pdrd_exceeded(self):
        return abs(self.current_diluate_rinse_pressure_difference()) > self.critical_value_dc

    def pdrd_exceeded_positive_sign(self):
        return self.current_diluate_rinse_pressure_difference() > 0

    def manage_pressures(self):

        if self.pddc_exceeded():

            self.pddc_large_time()
            # We adjust the desired flow values according to the sign of the PDDC
            if self.pddc_exceeded_positive_sign():
                if self.ed_massflow_diluate.desired_value * 0.95 >= 0.25:
                    self.ed_massflow_diluate.adjustment = self.ed_massflow_diluate.adjustment * 0.95
            else:
                if self.ed_massflow_concentrate.desired_value * 0.95 >= 0.25:
                    self.ed_massflow_concentrate.adjustment = self.ed_massflow_concentrate.adjustment * 0.95

        elif self.pddc_potential_problem:
            self.pddc_potential_problem = False
            print("THE PDDC HAS BEEN STABILIZED \n")

        if self.pdrd_exceeded():
            self.pdrd_problem = True
            # In case of a PDRD issue, the rinse hand valve needs to be adjusted
            if self.pdrd_exceeded_positive_sign():
                self.pdrd_problem_description = "TURN RIGHT"
            else:
                self.pdrd_problem_description = "TURN LEFT"


class ED:

    run_ed = True

    post_treatment_switch_off = False

    def __init__(self, update_list, apason_system):

        self.ed_pre_diluate_valve_name = conf.control_configurations["ed_general"]["ed_pre_diluate_valve_name"]
        self.ed_pre_concentrate_valve_name = conf.control_configurations["ed_general"]["ed_pre_concentrate_valve_name"]
        self.ed_post_diluate_valve_name = conf.control_configurations["ed_general"]["ed_post_diluate_valve_name"]
        self.ed_post_concentrate_valve_name = conf.control_configurations["ed_general"]["ed_post_concentrate_valve_name"]
        self.ed_second_pre_diluate_valve_name = conf.control_configurations["ed_general"]["ed_second_pre_diluate_valve_name"]
        self.ed_concentrate_dilute_valve_name = conf.control_configurations["ed_general"]["ed_concentrate_dilute_valve_name"]

        self.ed_con_tank_middle_ls_name = conf.control_configurations["ed_general"]["ed_con_tank_middle_ls_name"]
        self.ed_split_tank_middle_ls_name = conf.control_configurations["ed_general"]["ed_split_tank_middle_ls_name"]
        self.ed_split_tank_low_ls_name = conf.control_configurations["ed_general"]["ed_split_tank_low_ls_name"]
        self.ed_rinse_tank_ls_name = conf.control_configurations["ed_general"]["ed_rinse_tank_ls_name"]
        self.uf_tank_low_ls_name = conf.control_configurations["ed_general"]["uf_tank_low_ls_name"]
        self.ed_concentrate_conductivity_name = conf.control_configurations["ed_general"]["ed_concentrate_conductivity_name"]

        for sensor in update_list.levelswitch:
            if sensor.name == self.ed_con_tank_middle_ls_name:
                self.ed_con_tank_middle_ls = sensor
            elif sensor.name == self.ed_split_tank_middle_ls_name:
                self.ed_split_tank_middle_ls = sensor
            elif sensor.name == self.ed_split_tank_low_ls_name:
                self.ed_split_tank_low_ls = sensor
            elif sensor.name == self.ed_rinse_tank_ls_name:
                self.ed_rinse_tank_ls = sensor
            elif sensor.name == self.uf_tank_low_ls_name:
                self.uf_tank_low_ls = sensor

        for sensor in update_list.conductivity:
            if sensor.name == self.ed_concentrate_conductivity_name:
                self.ed_concentrate_conductivity = sensor

        for valve in apason_system.system_ocvs_nc:
            if valve.name == self.ed_concentrate_dilute_valve_name:
                self.ed_concentrate_dilute_valve = valve

        for valve in apason_system.system_cv3s:
            if valve.name == self.ed_pre_diluate_valve_name:
                self.ed_pre_diluate_valve = valve

            elif valve.name == self.ed_pre_concentrate_valve_name:
                self.ed_pre_concentrate_valve = valve

            elif valve.name == self.ed_post_diluate_valve_name:
                self.ed_post_diluate_valve = valve

            elif valve.name == self.ed_post_concentrate_valve_name:
                self.ed_post_concentrate_valve = valve

            elif valve.name == self.ed_second_pre_diluate_valve_name:
                self.ed_second_pre_diluate_valve = valve

        self.polarity = apason_system.polarity
        self.polarity.set_new_state("OFF")

        self.reversal_time = conf.control_configurations["ed_general"]["reversal_time"]

        self.starting_up = True
        self.uninitialized = True
        self.uf_ready = False

        self.too_concentrated = False

        self.massflow_concentrate = ED_Massflow_PI(update_list, apason_system, "ed_concentrate_flow")
        self.massflow_diluate = ED_Massflow_PI(update_list, apason_system, "ed_diluate_flow")
        self.massflow_rinse = ED_Massflow_PI(update_list, apason_system, "ed_rinse_flow")
        self.massflow_posttreatment = ED_Massflow_PI(update_list, apason_system, "ed_pt_flow")

        self.pressure_control = ED_Pressure_Control(update_list,
                                                    ed_massflow_diluate=self.massflow_diluate,
                                                    ed_massflow_concentrate=self.massflow_concentrate)

        self.conductivity_control = ED_Conductivity_PI(update_list, apason_system, "ed_conductivity",
                                                       ed_diluate_flow_control=self.massflow_diluate,
                                                       ed_concentrate_flow_control=self.massflow_concentrate,
                                                       ed_pt_flow_control=self.massflow_posttreatment)
        self.conductivity_count = 0


    def set_uf_ready(self):
        self.uf_ready = True


    def setup_reversal(self):

        # The valves need to be switched into Reversal mode

        self.ed_pre_diluate_valve.set_new_state("LOW")
        self.ed_pre_concentrate_valve.set_new_state("LOW")

        # Switching the polarity

        self.polarity.set_new_state("HIGH")  # "HIGH" == "NEG"
        self.last_polarity_switch_time = time.time()

        self.massflow_diluate.set_reversal_control()
        self.massflow_concentrate.set_reversal_control()

        # We let the pumps go before we switch the other two valves, to expel the "bad" water before we redirect the pathway

        self.massflow_diluate.massflow_pi()
        self.massflow_concentrate.massflow_pi()

        time.sleep(1)

        # We switch the last batch of valves

        self.ed_post_diluate_valve.set_new_state("HIGH")
        self.ed_post_concentrate_valve.set_new_state("HIGH")


    def setup_normal(self):

        # The valves need to be switched into Reversal mode

        self.ed_pre_diluate_valve.set_new_state("HIGH")
        self.ed_pre_concentrate_valve.set_new_state("HIGH")

        # Switching the polarity

        self.polarity.set_new_state("LOW") # "LOW" == "POS"
        self.last_polarity_switch_time = time.time()

        self.massflow_diluate.set_normal_control()
        self.massflow_concentrate.set_normal_control()

        # We let the pumps go before we switch the other two valves, to expel the "bad" water before we redirect the pathway

        self.massflow_diluate.massflow_pi()
        self.massflow_concentrate.massflow_pi()

        time.sleep(1)

        # We switch the last batch of valves

        self.ed_post_diluate_valve.set_new_state("LOW")
        self.ed_post_concentrate_valve.set_new_state("LOW")


    def startup_ed(self):
        # Assessing the state of the system at the beginning

        # All the tanks are filled, we can directly start outputting water
        if self.uf_ready & (self.ed_split_tank_middle_ls.current_value == "CLOSED"):
            self.ed_concentrate_dilute_valve.set_new_state("LOW")
            self.post_treatment = True
            self.starting_up = False
            print("STARTING UP ED WITH POST TREATMENT. \n")
        # All tanks but the split tank are filled. We need to fill it before we can start outputting water,
        # however, the electro-dialysis process can already commence.
        elif self.uf_ready & (self.ed_con_tank_middle_ls.current_value == "CLOSED"):
            self.ed_concentrate_dilute_valve.set_new_state("LOW")
            self.post_treatment = False
            self.starting_up = False
            print("STARTING UP ED NO POST TREATMENT. \n")
        # We do not have enough water in the UF tank to start the ED process and additionally,
        # we need more water in the concentrate to begin.
        elif self.ed_con_tank_middle_ls.current_value == "OPEN":
            self.ed_concentrate_dilute_valve.set_new_state("HIGH")
            print("OPENING VALVE TO FILL CONCENTRATION TANK. \n")

        else:
            print("ED IN IDLE \n")


    def initialize_ed(self):
        print("INITIALIZING ED…")
        if self.post_treatment:
            self.setup_normal()
            self.do_ed_no_pt()

            # Just ensuring the post-treatment pump doesn't start before the others
            time.sleep(1)

            self.massflow_posttreatment.massflow_pi()
        else:
            self.setup_normal()
            self.do_ed_no_pt()
        self.uninitialized = False


    def change_polarity(self):
        print("----------------- \nSETTING NEW POLARITY. \n")
        if self.polarity.state == "LOW" or self.polarity.state == "OFF": # currently normal, switch to reversal
            self.massflow_concentrate.stop_pump()
            self.massflow_diluate.stop_pump()
            self.setup_reversal()

        elif self.polarity.state == "HIGH":
            self.massflow_concentrate.stop_pump()
            self.massflow_diluate.stop_pump()
            self.setup_normal()

        else:
            print("Polarity is in an undefined state")
        self.last_polarity_switch_time = time.time()


    def concentration_tank(self):
        if (self.ed_concentrate_conductivity.current_value > 56) & (not self.too_concentrated):
            print("THE CONCENTRATE TANK IS TOO CONCENTRATED. WE'RE ADDING WATER IN FROM THE FEED TANK. \n" )
            # open dilute valve
            self.ed_concentrate_dilute_valve.set_new_state("HIGH")
            self.valve_opening_time = time.time()
            self.too_concentrated = True

        elif self.too_concentrated:

            if( (self.uf_tank_low_ls.current_value == "OPEN") | (time.time() - self.valve_opening_time > 30.0)):
                # close dilute valve
                print("THE UF TANK IS RUNNING LOW ON WATER OR THIRTY SECONDS HAVE PASSED. CLOSING THE VALVE AGAIN. \n")
                self.ed_concentrate_dilute_valve.set_new_state("LOW")
                self.too_concentrated = False
            else:
                print("DECONCENTRATION IN PROGRESS. " + str(time.time() - self.valve_opening_time) + " SECONDS HAVE PASSED. \n")

        else:
            print("CONCENTRATION TANK IS GOOD. \n")


    def do_ed_no_pt(self):
        # adjust the massflow of all pumps except the posttreatment pump
        print("\n \n DO ED NO PT! \n \n")
        self.massflow_concentrate.massflow_pi()
        self.massflow_diluate.massflow_pi()
        self.massflow_rinse.massflow_pi()


    def do_ed_with_pt(self):
        print("\n \n DO ED WITH PT! \n \n")
        # adjust the massflow of all pumps
        self.massflow_diluate.massflow_pi()
        self.massflow_rinse.massflow_pi()
        self.massflow_concentrate.massflow_pi()
        self.massflow_posttreatment.massflow_pi()


    # def do_pt_only(self):
    #     print("\n \n DO PT ONLY! \n \n")
    #     self.massflow_posttreatment.massflow_pi()


    def run_ed_cycle(self):

        print("\nCOMMENCING ED CYCLE")

        # Check all pressures

        self.pressure_control.manage_pressures()

        now = time.time()

        # Check if a polarity switch is necessary

        time_difference = (now - self.last_polarity_switch_time)
        print("ELAPSED TIME SINCE LAST POLARITY SWITCH: " + str(time_difference))
        if time_difference > self.reversal_time:
            self.change_polarity()

        # Check if the concentration tank concentration is all right

        self.concentration_tank()

        # Manage the pump flows

        self.do_massflow_control()

        # Manage the output conductivity

        self.do_conductivity_control()


    def do_conductivity_control(self):
        self.conductivity_control.conductivity_pi()


    def do_massflow_control(self):

        # Check if the output pump has been turned off manually via the GUI

        if self.post_treatment_switch_off:
            print("SWITCH ENGAGED, MUST STOP PT")
            # If we were previously using the PT pump, we need to stop now.
            if self.post_treatment:
                self.post_treatment = False
                self.massflow_posttreatment.stop_pump()
                self.do_ed_no_pt()
            else:
                self.do_ed_no_pt()

        elif self.ed_split_tank_middle_ls.current_value == "CLOSED":
            print("LEVELSWITCH CLOSED CAN DO PT")
            if self.post_treatment:
                self.do_ed_with_pt()
            # If we previously couldn't use the PT pump, we need to reset it now that we can.
            else:
                self.massflow_posttreatment.reset_pump_control()
                self.post_treatment = True
                self.do_ed_with_pt()
        else:
            print("LEVELSWITCH OPEN CANT DO PT")
            # If we previously were using the PT pump, we need to stop now.
            if self.post_treatment:
                self.massflow_posttreatment.stop_pump()
                self.post_treatment = False
                self.do_ed_no_pt()
            else:
                self.do_ed_no_pt()


    def turn_off_ed(self):

        # Turn off all ED instruments.

        print("-------------\nSHUTTING DOWN THE ED! \n")
        self.massflow_concentrate.stop_pump()
        self.massflow_rinse.stop_pump()
        self.massflow_diluate.stop_pump()
        self.massflow_posttreatment.stop_pump()

        self.ed_pre_diluate_valve.set_new_state("LOW")
        self.ed_pre_concentrate_valve.set_new_state("LOW")
        self.ed_post_diluate_valve.set_new_state("LOW")
        self.ed_post_concentrate_valve.set_new_state("LOW")
        self.ed_concentrate_dilute_valve.set_new_state("LOW")
        self.ed_second_pre_diluate_valve.set_new_state("LOW")
        self.polarity.set_new_state("OFF")


    def control_ed(self):

        if self.run_ed:
            if self.starting_up:
                self.startup_ed()
            elif self.uninitialized:
                self.initialize_ed()
            else:
                self.run_ed_cycle()
        else:
            self.turn_off_ed()
