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

class UF:
    """
    **PI-control** \n
    **Properties:** run_uf (bool), control_instrument_name, K_p, K_i, desired_value, integral, output, non_saturated_output \n
    **Functions:** control_UF_Feed_Flow() (while loop until run_uf==False) \n
    """
    run_uf = True
    control_instrument_name = "UF Feed Pump"

    def __init__(self, update_list, apason_system):

        self.system = apason_system
        self.back_flush = False
        self.first_loop = True

        self.massflow_control_configuration = conf.control_configurations["uf_massflow_control"]
        self.backflush_configuration = conf.control_configurations["uf_backflush"]

        self.K_p = self.massflow_control_configuration["K_p"]
        self.K_i = self.massflow_control_configuration["K_i"]
        self.desired_value = self.massflow_control_configuration["desired_value"]
        self.integral = 0.0
        self.pump_output = 0.0 #in Volt!
        self.non_saturated_input = 0.0

        self.max_tmp = self.backflush_configuration["switch_value"]


        self.control_value_sensor_name = self.massflow_control_configuration["control_value_sensor_name"]
        self.feed_pressure_name = self.backflush_configuration["control_value_sensor_name_1"]
        self.permeate_pressure_name = self.backflush_configuration["control_value_sensor_name_2"]

        # Find corresponding sensor for massflow control in the update list
        for sensor in update_list.massflow:
            if sensor.name == self.control_value_sensor_name:
                self.control_value_sensor: ul.Update_List_Massflow = sensor

        # Find corresponding pump for massflow control in the system
        for control_instrument in self.system.system_pumps:
            if control_instrument.name == self.control_instrument_name:
                self.control_instrument = control_instrument

        # Find pressure sensors for TMP
        for sensor in update_list.pressure:
            if sensor.name == self.feed_pressure_name:
                self.feed_pressure_sensor : ul.Update_List_Pressure = sensor
            if sensor.name == self.permeate_pressure_name:
                self.permeate_pressure_sensor: ul.Update_List_Pressure = sensor




    def control_UF(self):
        # TODO :)
        while self.run_uf:
            while self.back_flush == False:

                self.uf_feed_massflow_control()

                self.check_for_backflush()

                time.sleep(1)

            self.backflush()

    def uf_feed_massflow_control(self):

        if self.first_loop:
            self.time_start = time.time()  # current time in seconds
            self.time_current = self.time_start
            elapsed_time = self.time_start - self.system.time_start
            self.first_loop = False
            # ignore stopIdentifier for now, that's for backwash
        else:
            self.time_current = time.time()
            elapsed_time = self.time_current - self.time_last

        last_measurement = self.control_value_sensor.current_value
        error = self.desired_value - last_measurement

        # Proportional Controller
        P_out = self.K_p * error

        # Integrative Controller
        if self.non_saturated_input is not self.pump_output:
            I_out = 0.0
        else:
            self.integral = self.integral + elapsed_time * error
            I_out = self.K_i * self.integral
        out = P_out + I_out

        # control adder
        self.pump_output = self.pump_output + out

        # Do this before possible saturation
        self.non_saturated_input = self.pump_output

        # make sure we aren't already at the maximum or below 0: saturation check
        if self.pump_output > self.control_instrument.max_RPM:
            self.pump_output = 5.0
        elif self.pump_output < 0.0:
            self.pump_output = 0.0

        self.control_instrument.set_new_state(self.control_instrument.voltage_to_rpm(self.pump_output))
        self.time_last = self.time_current

    def check_for_backflush(self):
        self.find_tmp()

        #or other conditions
        if self.tmp >= self.max_tmp:
            self.back_flush = True
            self.first_loop = True

    def backflush(self):
        # TODO
        pass

    def find_tmp(self):
        self.tmp = self.feed_pressure_sensor.current_value - self.permeate_pressure_sensor.current_value

# TODO
class ED:
    run_ed = False

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
        self.overall_control_thread = Timer(2.0, function=self.run_test)
        self.overall_control_thread.start()

    def run_test(self):
        pass
        # uf = UF(self.update_list, self.system)
        # uf.control_UF()

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
