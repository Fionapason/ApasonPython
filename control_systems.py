import configurations_control as conf
import Sensor_Update_List as ul
from threading import Thread, Timer
import time

"""
Here all control systems are initiated, and their control loops are defined. They take their specifications from the configurations_control file.

A PI control system routinely compares a specific sensor's measured value with a set desired value, and based on the difference,
adapts the input of a specific control instrument accordingly.

They take update_list as a parameter and find their corresponding control value sensor by checking the update_list sensors' properties for the right name.

They also take apason_system as a parameter and use it to find their corresponding control instrument.

All control systems are subtasks of the overall_control thread, which is run by apason_system.
"""


# PI-control
# Properties: run_uf (bool), control_instrument_name, K_p, K_i, desired_value, integral, output, non_saturated_output
# Functions: control_UF_Feed_Flow() (while loop)
class UF_Massflow_PI:
    """
    **PI-control** \n
    **Properties:** run_uf (bool), control_instrument_name, K_p, K_i, desired_value, integral, output, non_saturated_output \n
    **Functions:** control_UF_Feed_Flow() (while loop until run_uf==False) \n
    """

    K_p : float
    K_i : float
    desired_value : float
    integral : float
    non_saturated_output : float
    pump_output : float # in Volt!

    first_loop = True

    control_value_sensor_name : str # Massflow sensor
    control_instrument_name : str # Pump
    steady_state_tmp_set = False

    def __init__(self, update_list, apason_system, control_configuration : str, tmp, backwash=False):

        self.K_p = conf.control_configurations[control_configuration]["K_p"]
        self.K_i = conf.control_configurations[control_configuration]["K_i"]
        self.desired_value = conf.control_configurations[control_configuration]["desired_value"]
        self.integral = 0.0
        self.pump_output = 0.0
        self.non_saturated_output = 0.0
        self.system_time_start = apason_system.time_start

        self.control_value_sensor_name = conf.control_configurations[control_configuration]["control_value_sensor_name"]
        self.control_instrument_name = conf.control_configurations[control_configuration]["control_instrument_name"]

        for sensor in update_list.massflow:
            if sensor.name == self.control_value_sensor_name:
                self.control_value_sensor: ul.Update_List_Massflow = sensor
                break

        for instrument in apason_system.system_pumps:
            if instrument.name == self.control_instrument_name:
                self.control_instrument = instrument
                break

        self.tmp_control : UF_TMP_Control = tmp
        self.backwash = backwash



    def stop_pump(self):
        self.control_instrument.set_new_state(0.0)
        print(self.control_instrument_name + " SET TO 0.")

    def reset_pump_control(self):
        print("RESETTING " + self.control_instrument_name)

        self.integral = 0.0
        self.pump_output = 0.0  # in Volt!
        self.non_saturated_output = 0.0
        self.system_time_start = time.time()
        self.steady_state_tmp_set = False
        self.first_loop = True

    def massflow_pi(self):

        if not self.backwash:
            if (not self.steady_state_tmp_set) and (time.time() - self.system_time_start > 60):
                self.steady_state_tmp_limit = self.tmp_control.current_trans_membrane_pressure() + 0.2 # bar
                self.steady_state_tmp_set = True
                print("STEADY STATE TMP LIMIT SET TO: " + str(self.steady_state_tmp_limit) + " BAR \n")

            if self.steady_state_tmp_set and self.tmp_control.tmp_exceeded(self.steady_state_tmp_limit):
                print("TMP EXCEEDED! \n")
                print("TMP WAS " + str(self.tmp_control.current_trans_membrane_pressure()))
                return

        if self.first_loop:
            self.time_start = time.time()  # current time in seconds
            self.time_current = self.time_start
            elapsed_time = self.time_start - self.system_time_start
            self.first_loop = False
        else:
            self.time_current = time.time()
            elapsed_time = self.time_current - self.time_last

        last_measurement = self.control_value_sensor.current_value
        error = self.desired_value - last_measurement

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

        print("Setting " + self.control_instrument_name + " to Voltage: " + str(self.pump_output))

        self.control_instrument.set_new_state(self.control_instrument.voltage_to_rpm(self.pump_output))
        self.time_last = self.time_current

        time.sleep(2) # Waiting time

class UF_TMP_Control:

    switch_value : float

    feed_pressure_sensor_name : str
    permeate_pressure_sensor_name : str


    def __init__(self, update_list):

        self.switch_value = conf.control_configurations["uf_tmp"]["switch_value"]

        self.feed_pressure_sensor_name = conf.control_configurations["uf_tmp"]["feed_pressure_sensor_name"]
        self.permeate_pressure_sensor_name = conf.control_configurations["uf_tmp"]["permeate_pressure_sensor_name"]

        for sensor in update_list.pressure:
            if sensor.name == self.feed_pressure_sensor_name:
                self.feed_pressure_sensor: ul.Update_List_Pressure = sensor
            elif sensor.name == self.permeate_pressure_sensor_name:
                self.permeate_pressure_sensor: ul.Update_List_Pressure = sensor

    def current_trans_membrane_pressure(self):
        feed_pressure = self.feed_pressure_sensor.current_value
        permeate_pressure = self.permeate_pressure_sensor.current_value
        tmp = abs(feed_pressure - permeate_pressure)
        return tmp

    def tmp_exceeded(self, max=0.8):
        current_tmp = self.current_trans_membrane_pressure()
        print("CURRENT TMP: " + str(current_tmp) + " BAR \n")
        if current_tmp >= self.switch_value:
            print("TMP EXCEEDED 0.8 BAR! \n")
            return True
        else:
            if current_tmp >= max:
                print("TMP EXCEEDED STEADY STATE TMP BY MORE THAN 0.2 BAR! \n")
                return True
            return False

class UF:

    run_uf = True

    uf_backwash_valve_name : str
    uf_feed_valve_name :  str
    uf_switch_valve_name : str

    uf_tank_high_ls_name : str
    uf_tank_middle_ls_name: str
    uf_tank_low_ls_name: str

    backwash_time : float

    process : str

    def __init__(self, update_list, apason_system):

        self.uf_backwash_valve_name = conf.control_configurations["uf_general"]["uf_backwash_valve_name"]
        self.uf_feed_valve_name = conf.control_configurations["uf_general"]["uf_feed_valve_name"]
        self.uf_switch_valve_name = conf.control_configurations["uf_general"]["uf_switch_valve_name"]

        self.uf_tank_high_ls_name = conf.control_configurations["uf_general"]["uf_tank_high_ls_name"]
        self.uf_tank_middle_ls_name = conf.control_configurations["uf_general"]["uf_tank_middle_ls_name"]
        self.uf_tank_low_ls_name = conf.control_configurations["uf_general"]["uf_tank_low_ls_name"]

        self.backwash_time = conf.control_configurations["uf_general"]["backwash_time"]

        for sensor in update_list.levelswitch:
            if sensor.name == self.uf_tank_high_ls_name:
                self.uf_tank_high_ls = sensor
            elif sensor.name == self.uf_tank_middle_ls_name:
                self.uf_tank_middle_ls = sensor
            elif sensor.name == self.uf_tank_low_ls_name:
                self.uf_tank_low_ls = sensor

        for valve in apason_system.system_ocvs_nc:
            if valve.name == self.uf_backwash_valve_name:
                self.uf_backwash_valve = valve

        for valve in apason_system.system_ocvs_no:
            if valve.name == self.uf_feed_valve_name:
                self.uf_feed_valve = valve

        for valve in apason_system.system_cv3s:
            if valve.name == self.uf_switch_valve_name:
                self.uf_switch_valve = valve

        self.tmp_control = UF_TMP_Control(update_list)

        self.massflow_backwash = UF_Massflow_PI(update_list, apason_system, "uf_backwash_flow", self.tmp_control, backwash=True)

        self.massflow_feed = UF_Massflow_PI(update_list, apason_system, "uf_feed_flow", self.tmp_control)

        self.process = 'FEED'

        self.setup_feed()

        self.start_ED = False
        self.is_ED_set = False

    def set_process(self):

        if self.tmp_control.tmp_exceeded():
            self.massflow_feed.stop_pump()
            self.setup_backwash()
            self.massflow_backwash.reset_pump_control()
            self.process = 'BACKWASH'
            print("SWITCHING TO BACKWASH \n")

        elif self.process == 'BACKWASH':
            if self.uf_tank_middle_ls.current_value == "CLOSED":
                self.massflow_backwash.stop_pump()
                self.setup_feed()
                self.process = 'IDLE'
                print("THERE IS ENOUGH WATER IN THE TANK. TURNING OFF UF. \n")
            else:
                self.setup_feed()
                self.massflow_backwash.stop_pump()
                self.massflow_feed.reset_pump_control()
                self.process = 'FEED'
                print("WE'RE LOW ON WATER + BACKWASH IS DONE. SWITCHING TO FEED. \n")

        elif self.process == 'IDLE':
            if self.uf_tank_middle_ls.current_value == "OPEN":
                self.setup_feed()
                self.massflow_feed.reset_pump_control()
                self.process = 'FEED'
                print("WE'RE LOW ON WATER. SWITCHING TO FEED. \n")

        elif self.process == 'FEED':
            if self.uf_tank_high_ls.current_value == "CLOSED":
                self.massflow_feed.stop_pump()
                self.setup_backwash()
                self.massflow_backwash.reset_pump_control()
                self.process = 'BACKWASH'
                print("TOO MUCH WATER IN TANK. SWITCHING TO BACKWASH \n")



    def setup_feed(self):
        self.uf_backwash_valve.set_new_state("LOW")
        self.uf_switch_valve.set_new_state("LOW")
        self.uf_feed_valve.set_new_state("LOW")
        print("VALVES SET TO FEED \n")

    def setup_backwash(self):
        self.uf_feed_valve.set_new_state("HIGH")
        self.uf_switch_valve.set_new_state("HIGH")
        self.uf_backwash_valve.set_new_state("HIGH")
        print("VALVES SET TO BACKWASH \n")

    def do_feed(self):
        self.massflow_feed.massflow_pi()


    def do_backwash(self):
        print("Starting backwash!")
        start = time.time()
        current = start

        while (current - start < self.backwash_time):
            self.massflow_backwash.massflow_pi()
            current = time.time()
            print(str(current - start) + " SECONDS OF BACKWASH PASSED. \n")

        self.massflow_backwash.stop_pump()

    def set_ED(self):
        if self.is_ED_set:
            return
        if self.uf_tank_middle_ls.current_value == "OPEN":
            self.start_ED = False
        if self.uf_tank_middle_ls.current_value == "CLOSED":
            self.start_ED = True
            self.is_ED_set = True

    def control_UF(self):

        while self.run_uf:
            # check if we can start ED
            self.set_ED()

            # decide on current state
            self.set_process()

            if self.process == 'BACKWASH':
                self.do_backwash()
            elif self.process == 'FEED':
                self.do_feed()
            elif self.process == 'IDLE':
                continue

            time.sleep(2)


class ED_Pressure_Control:
    pass

class ED:
    run_ed = False

    def __init__(self, update_list, apason_system):

        self.ed_pre_diluate_valve_name = conf.control_configurations["ed_general"]["ed_pre_diluate_valve_name"]
        self.ed_pre_concentrate_valve_name = conf.control_configurations["ed_general"]["ed_pre_concentrate_valve_name"]
        self.ed_post_diluate_valve_name = conf.control_configurations["ed_general"]["ed_post_diluate_valve_name"]
        self.ed_post_concentrate_valve_name = conf.control_configurations["ed_general"]["ed_post_concentrate_valve_name"]
        self.ed_second_pre_diluate_valve_name = conf.control_configurations["ed_general"]["ed_second_pre_diluate_valve_name"]
        self.ed_concentrate_dilute_valve_name = conf.control_configurations["ed_general"]["ed_concentrate_dilute_name"]

        self.ed_con_tank_high_ls_name = conf.control_configurations["ed_general"]["ed_con_tank_high_ls_name"]
        self.ed_con_tank_middle_ls_name = conf.control_configurations["ed_general"]["ed_con_tank_middle_ls_name"]
        self.ed_split_tank_middle_ls_name = conf.control_configurations["ed_general"]["ed_split_tank_middle_ls_name"]
        self.ed_split_tank_low_ls_name = conf.control_configurations["ed_general"]["ed_split_tank_low_ls_name"]
        self.ed_rinse_tank_ls_name = conf.control_configurations["ed_general"]["ed_rinse_tank_ls_name"]
        self.uf_tank_low_ls_name = conf.control_configurations["ed_general"]["uf_tank_low_ls_name"]

        for sensor in update_list.levelswitch:
            if sensor.name == self.ed_con_tank_high_ls_name:
                self.ed_con_tank_high_ls = sensor
            elif sensor.name == self.ed_con_tank_middle_ls_name:
                self.ed_con_tank_middle_ls = sensor
            elif sensor.name == self.ed_split_tank_middle_ls_name:
                self.ed_split_tank_middle_ls = sensor
            elif sensor.name == self.ed_split_tank_low_ls_name:
                self.ed_split_tank_low_ls = sensor
            elif sensor.name == self.ed_rinse_tank_ls_name:
                self.ed_rinse_tank_ls = sensor
            elif sensor.name == self.uf_tank_low_ls_name:
                self.uf_tank_low_ls = sensor

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
        self.uf_ready = False

    def UF_ready(self):
        self.uf_ready = True

    def setup_reversal(self):
        self.ed_pre_diluate_valve.set_new_state("LOW")
        self.ed_pre_concentrate_valve.set_new_state("LOW")
        self.ed_post_diluate_valve.set_new_state("HIGH")
        self.ed_post_concentrate_valve.set_new_state("HIGH")

        self.polarity.set_new_state("HIGH") # "HIGH" == "NEG"

    def setup_normal(self):
        self.ed_pre_diluate_valve.set_new_state("HIGH")
        self.ed_pre_concentrate_valve.set_new_state("HIGH")
        self.ed_post_diluate_valve.set_new_state("LOW")
        self.ed_post_concentrate_valve.set_new_state("LOW")

        self.polarity.set_new_state("LOW") # "LOW" == "POS"

    def startup_ED(self):

        # All the tanks are filled
        if self.uf_ready & self.ed_split_tank_middle_ls.current_value == "CLOSED":
            self.ed_concentrate_dilute_valve.set_new_state("LOW")
            self.post_treatment = True
            # conc tank control
            self.starting_up = False

        elif self.uf_ready & self.ed_con_tank_middle_ls.current_value == "CLOSED":
            self.ed_concentrate_dilute_valve.set_new_state("LOW")
            self.post_treatment = False
            # conc tank control
            self.starting_up = False

        elif self.ed_con_tank_high_ls.current_value == "OPEN":
            self.ed_concentrate_dilute_valve.set_new_state("HIGH")

    def initialize_ED(self):
        if self.post_treatment:
            self.setup_normal()
            #start Pumps with MF control, wait 1 second for PT pump
        else:
            self.setup_normal()
            #start Pumps with MF control, except PT pump


    def change_polarity(self):
        if self.polarity.state == "LOW": # currently normal, switch to reversal
            #Stop diluate and concentrate pumps
            self.setup_reversal()
            #Start diluate and concentrate pumps
        if self.polarity.state == "HIGH":
            #Stop diluate and concentrate pumps
            self.setup_normal()
            #Start diluate and concentrate pumps
        self.last_polarity_switch_time = time.time()

    def

    def run_ED(self):

        # check pressures

        now = time.time()

        if now - self.last_polarity_switch_time > self.reversal_time:
            self.change_polarity()

        if self.ed_split_tank_middle_ls.current_value == "CLOSED":
            if self.post_treatment:
                pass
               #massflow control all pumps
            else:
                # start pt pump
                self.post_treatment = True
                # massflow control all pumps
        else:
            if self.post_treatment:
                # stop pt pump
                self.post_treatment = False
                # massflow control pumps except pt
            else:
                pass
                # massflow control pumps except pt



    def control_ED(self):
        if self.starting_up:
            self.startup_ED()
            if not self.starting_up:
                self.initialize_ED()
        else:
            self.run_ED()

# Parameters: overall_control_thread, run_overall = True
# Function: run_test()
class Overall_Control:
    """
    **Parameters:** overall_control_thread, run_overall = True \n
    **Function:** run_test()
    """
    overall_control_thread: Timer
    run_overall = True

    def __init__(self, update_list, apason_system):
        self.system = apason_system
        self.update_list = update_list
        self.uf = UF(self.update_list, self.system)
        self.overall_control_thread = Timer(2.0, function=self.run_test)
        self.overall_control_thread.start()

        self.ed = ED(self.update_list, self.system)

    def run_test(self):
        while (self.run_overall):
            self.uf.control_UF()
            if self.uf.start_ED:
                self.ed.UF_ready()
                self.ed.control_ED()

    # TODO
    def check_if_UF(self):
        pass

    # TODO
    def check_if_ED(self):
        pass

    def stop(self):
        self.overall_control_thread.join()


if __name__ == '__main__':
    pass
