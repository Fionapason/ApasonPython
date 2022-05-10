import configurations_control as conf
import Sensor_Update_List as ul
from threading import Thread, Timer
import time

from timeloop import Timeloop
from datetime import timedelta
from ischedule import schedule, run_loop

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

        self.configuration = conf.control_system_configurations["uf_massflow_control"]
        self.K_p = self.configuration["K_p"]
        self.K_i = self.configuration["K_i"]
        self.desired_value = self.configuration["desired_value"]
        self.integral = 0.0
        self.output = 0.0 #in Volt!
        self.non_saturated_input = 0.0
        self.system = apason_system

        self.control_value_sensor_name = self.configuration["control_value_sensor_name"]

        # Find corresponding sensor from the update list
        for sensor in update_list.massflow:
            if sensor.name == self.control_value_sensor_name:
                self.control_value_sensor: ul.Update_List_Massflow = sensor

        # Find corresponding control instrument in the system
        for control_instrument in self.system.system_pumps:
            if control_instrument.name == self.control_instrument_name:
                self.control_instrument = control_instrument

        self.count = 0

    def control_UF_Feed_Flow(self):
        while self.run_uf:
            if self.count == 0:
                self.time_start = time.time()  # current time in seconds
                self.time_current = self.time_start
                elapsed_time = self.time_start - self.system.time_start
                # ignore stopIdentifier for now, that's for backwash
            else:
                self.time_current = time.time()
                elapsed_time = self.time_current - self.time_last

            last_measurement = self.control_value_sensor.current_value

            error = self.desired_value - last_measurement

            # Proportional Controller
            P_out = self.K_p * error

            # Integrative Controller
            if self.non_saturated_input is not self.output:
                I_out = 0.0
            else:
                self.integral = self.integral + elapsed_time * error
                I_out = self.K_i * self.integral


            out = P_out + I_out

            # control adder
            self.output = self.output + out

            #Do this before possible saturation
            self.non_saturated_input = self.output

            # make sure we aren't already at the maximum or below 0
            # Conditional saturation
            if self.output > self.control_instrument.max_RPM:
                self.output = 5.0
            elif self.output < 0.0:
                self.output = 0.0



            self.control_instrument.set_new_state(self.control_instrument.voltage_to_rpm(self.output))

            self.time_last = self.time_current

            self.count += 1

            # print("1s job current time : {}".format(time.ctime()))
            time.sleep(1)

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
        # uf.control_UF_Feed_Flow()


if __name__ == '__main__':
    pass
