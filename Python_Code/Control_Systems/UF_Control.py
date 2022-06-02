import time

from Sensor_Instrument_Tracking import Sensor_Update_List as ul
from Configurations import Configurations_Control_Systems as conf

"""
Here the UF-specific sub-control systems are implemented as classes, as well as the UF's general control system.

The UF_Massflow_PI class uses a Proportional-Integral controller to maintain a steady massflow from all four of its pumps.
The PI controller checks the current massflow and, using experimentally determined K_p and K_i parameters,
adjusts the voltage set at the DAC output, which determines the pump force.

The UF_TMP_Control class keeps track of the current trans membrane pressure and checks if it is too high.

The UF class manages the general control of the UF module and effectively runs it, using instances of the aforementioned classes,
as well as tracking its own sensors as well.

"""

class UF_Massflow_PI:

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

        # We're only checking the TMP when we're not a backwashing pump.
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
            self.time_last = self.time_current
            elapsed_time = self.time_start - self.system_time_start
            self.first_loop = False
        else:
            self.time_current = time.time()
            elapsed_time = self.time_current - self.time_last
        if elapsed_time > 1.0:
            last_measurement = self.control_value_sensor.current_value
            print("CURRENT UF PERMEATE FLOW: " + str(last_measurement))
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

            # Control adder
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


class UF_TMP_Control:

    switch_value : float

    feed_pressure_sensor_name : str
    permeate_pressure_sensor_name : str

    tmp_problem = False


    def __init__(self, update_list):

        # The pressure at which we need to initiate a back-washing cycle
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
            self.tmp_problem = True
            return True
        else:
            if current_tmp >= max:
                print("TMP EXCEEDED STEADY STATE TMP BY MORE THAN 0.2 BAR! \n")
                self.tmp_problem = True
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
        self.currently_backwash = False

        self.critically_low_uf_tank_problem = False


    def set_process(self):


        if self.process == 'BACKWASH':
            if self.currently_backwash:
                # if we are doing a backwash because of the TMP, and the UF tank is low on water,
                # we need to stop in order to not suck air into the pump
                print("WE ARE BACKWASHING. \n THE LOWEST LEVELSWITCHES LEVEL IS: " + self.uf_tank_low_ls.current_value)
                if self.uf_tank_low_ls.current_value == "OPEN":
                    self.currently_backwash = False
                    self.massflow_backwash.stop_pump()
                    time.sleep(0.1)
                    self.setup_feed()
                    self.process = 'IDLE'
                    print("UF TANK IS CRITICALLY LOW. SHUTTING OFF BACKWASH. FILL IT MANUALLY, IF POSSIBLE.")
                    self.critically_low_uf_tank_problem = True
                else: # so that we can do backwash continuously, no new setup
                    return

            # We did a full 90-second cycle
            elif self.uf_tank_middle_ls.current_value == "CLOSED":
                self.massflow_backwash.stop_pump()
                time.sleep(0.1)
                self.setup_feed()
                self.process = 'IDLE'
                print("THERE IS ENOUGH WATER IN THE TANK. TURNING OFF UF. \n")
            else:
                self.massflow_backwash.stop_pump()
                time.sleep(0.1)
                self.setup_feed()
                self.massflow_feed.reset_pump_control()
                self.process = 'FEED'
                print("WE'RE LOW ON WATER + BACKWASH IS DONE. SWITCHING TO FEED. \n")

        elif self.tmp_control.tmp_exceeded():
            if self.critically_low_uf_tank_problem:
                print("HELP!!!")
            elif self.currently_backwash:
                pass
            else:
                self.massflow_feed.stop_pump()
                time.sleep(0.1)
                self.setup_backwash()
                self.massflow_backwash.reset_pump_control()
                self.process = 'BACKWASH'
                print("SWITCHING TO BACKWASH \n")

        elif self.process == 'IDLE':
            if self.critically_low_uf_tank_problem:
                pass
            elif self.uf_tank_middle_ls.current_value == "OPEN":
                self.setup_feed()
                time.sleep(0.1)
                self.massflow_feed.reset_pump_control()
                self.process = 'FEED'
                print("WE'RE LOW ON WATER. SWITCHING TO FEED. \n")

        elif self.process == 'FEED':
            if self.uf_tank_high_ls.current_value == "CLOSED":
                self.massflow_feed.stop_pump()
                time.sleep(0.1)
                self.setup_backwash()
                self.massflow_backwash.reset_pump_control()
                self.process = 'BACKWASH'
                print("TOO MUCH WATER IN TANK. SWITCHING TO BACKWASH \n")


    def setup_feed(self):
        # Changing our valves for feed
        self.uf_backwash_valve.set_new_state("LOW")
        self.uf_switch_valve.set_new_state("LOW")
        self.uf_feed_valve.set_new_state("LOW")
        print("VALVES SET TO FEED \n")


    def setup_backwash(self):
        # Changing our valves for backwash
        self.uf_feed_valve.set_new_state("HIGH")
        self.uf_switch_valve.set_new_state("HIGH")
        self.uf_backwash_valve.set_new_state("HIGH")
        print("VALVES SET TO BACKWASH \n")


    def do_feed(self):
        self.massflow_feed.massflow_pi()


    def do_backwash(self):

        current = time.time()

        # A backwashing cycle only lasts 90 seconds, so we need to keep track of how much time has passed.

        if not self.currently_backwash:
            print("Starting backwash!")
            self.backwash_start_time = current
            self.currently_backwash = True
            self.massflow_backwash.massflow_pi()

        else:
            if (current - self.backwash_start_time < self.backwash_time):
                self.massflow_backwash.massflow_pi()
                current = time.time()
                print(str(current - self.backwash_start_time) + " SECONDS OF BACKWASH PASSED. \n")
            else:
                self.currently_backwash = False
                self.massflow_backwash.stop_pump()


    def set_ed(self):

        # The UF needs to have reached a certain level to be able to give a green light for the ED

        if self.is_ED_set:
            return
        if self.uf_tank_middle_ls.current_value == "OPEN":
            self.start_ED = False
            print("UF NOT READY \n")
        if self.uf_tank_middle_ls.current_value == "CLOSED":
            print("uf tank middle levelswitch :" + self.uf_tank_middle_ls.current_value)
            self.start_ED = True
            self.is_ED_set = True
            print("UF READY \n")


    def control_uf(self):
        if self.run_uf:
                # check if we can start ED
                self.set_ed()

                # decide on current state
                self.set_process()

                if self.process == 'BACKWASH':
                    self.do_backwash()
                elif self.process == 'FEED':
                    self.do_feed()
                elif self.process == 'IDLE':
                    print("UF IS IDLING")
        else:
            self.turn_off_uf()
            self.start_ED = False
            self.is_ED_set = False


    def turn_off_uf(self):
        # Turn off all UF instruments
        print("-------------\nSHUTTING DOWN THE UF! \n")
        self.massflow_backwash.stop_pump()
        self.massflow_feed.stop_pump()
        self.uf_feed_valve.set_new_state("LOW")
        self.uf_backwash_valve.set_new_state("LOW")
        self.uf_switch_valve.set_new_state("LOW")
