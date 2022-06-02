from Configurations import Configurations_Control_Systems as conf
from threading import Timer
from Sensor_Instrument_Tracking import Apason_System_Instruments as apason
import time

from Control_Systems.ED_Control import ED
from Control_Systems.UF_Control import UF

"""
Here the overall control system is initiated. It takes its specifications from the configurations_control file.
It has its own sensors, which it checks independently, and also runs instances of the UF and ED control classes.
Overall_Control is responsible for managing pressure issues, which require either warning windows or complete system shut downs.

It is Apason_System, which in fact turns on the overall control thread.

The problems identified in the ED and UF control
"""


class Overall_Control:
    """
    **Parameters:** overall_control_thread, run_overall = True \n
    **Function:** run_test()
    """
    overall_control_thread: Timer
    run_overall = True
    stop_control = False


    def __init__(self, update_list, apason_system):

        print("INITIALIZING CONTROL!")

        self.system : apason.Apason_System() = apason_system
        self.update_list = update_list

        self.overall_feed_tank_high_ls_name = conf.control_configurations["overall_control"][
            "overall_feed_tank_high_ls_name"]
        self.overall_feed_tank_middle_ls_name = conf.control_configurations["overall_control"][
            "overall_feed_tank_middle_ls_name"]
        self.overall_feed_tank_low_ls_name = conf.control_configurations["overall_control"][
            "overall_feed_tank_low_ls_name"]

        self.overall_purge_tank_middle_ls_name = conf.control_configurations["overall_control"][
            "overall_purge_tank_middle_ls_name"]
        self.overall_purge_tank_high_ls_name = conf.control_configurations["overall_control"][
            "overall_purge_tank_high_ls_name"]

        self.overall_rinse_tank_ls_name = conf.control_configurations["overall_control"]["overall_rinse_tank_ls_name"]

        for sensor in update_list.levelswitch:

            if sensor.name == self.overall_feed_tank_high_ls_name:
                self.overall_feed_tank_high_ls = sensor

            elif sensor.name == self.overall_feed_tank_middle_ls_name:
                self.overall_feed_tank_middle_ls = sensor

            elif sensor.name == self.overall_feed_tank_low_ls_name:
                self.overall_feed_tank_low_ls = sensor

            elif sensor.name == self.overall_purge_tank_middle_ls_name:
                self.overall_purge_tank_middle_ls = sensor
            elif sensor.name == self.overall_purge_tank_high_ls_name:
                self.overall_purge_tank_high_ls = sensor
            elif sensor.name == self.overall_rinse_tank_ls_name:
                self.overall_rinse_tank_ls = sensor

        self.uf = UF(self.update_list, self.system)
        self.ed = ED(self.update_list, self.system)

        self.overall_state = "GOOD"

        self.overall_control_thread = Timer(5.0, function=self.run_control_systems)
        self.overall_control_thread.start()


    def run_control_systems(self):

        print("RUNNING CONTROL!")

        while (True):

            if self.stop_control:
                break

            while (self.run_overall):

                # Run every step of UF control

                self.uf.control_uf()

                # Check if ED can be done

                if self.uf.start_ED:
                    self.ed.set_uf_ready()

                # Run every step of ED control

                self.ed.control_ed()

                # Check our tank levels

                self.check_tanks()

                # Check if any pressures are bad

                self.pressure_problems()

                time.sleep(1)

    def pressure_problems(self):

        # Aside from specific pressure differences, there are additionally absolute pressure values that should not be exceeded.
        # Each sensor is assigned such a value, in its configuration, which is checked here.

        for sensor in self.update_list.pressure:
            if sensor.current_value > sensor.critical_pressure:
                print("HIGH PRESSURE IN PRESSURE SENSOR " + sensor.name + ": " + str(sensor.current_value))
                self.system.system_problem = "HIGH_PRESSURE"
                self.stop_server()
                return


        if time.time() - self.system.time_start < 30.0:
            return

        # If there is a problem we need to immediately shut down the system and inform the GUI what problem it is
        if self.ed.pressure_control.pddc_problem:
            print("SHUTTING DOWN. PDDC PROBLEM")
            self.stop_server()
            self.ed.pressure_control.pddc_problem = False
            self.system.system_problem = "PDDC"
            return
        if self.ed.pressure_control.pdrd_problem:
            print("SHUTTING DOWN. PDRD PROBLEM")
            print(self.ed.pressure_control.pdrd_problem_description)
            self.stop_server()
            self.ed.pressure_control.pddc_problem = False
            self.system.system_problem = "PDRD"
            return

        if self.uf.tmp_control.tmp_problem:
            print("SHUTTING DOWN. TMP PROBLEM")
            self.stop_server()
            self.ed.pressure_control.pddc_problem = False
            self.system.system_problem = "TMP"
            return



    def check_tanks(self):

        # Assessing all our tanks.

        if self.overall_feed_tank_low_ls.current_value == "OPEN":
            print("THE FEED TANK IS EMPTY. SHUTTING DOWN SYSTEM.")

            print("SHOWN ON LEVEL SWITCH " + self.overall_feed_tank_low_ls.name + " #" + str(self.overall_rinse_tank_ls.id) + "!!")
            print("OTHER LEVEL SWITCHES: \n" + self.overall_feed_tank_high_ls.name + ": " + str(self.overall_feed_tank_high_ls.current_value) + "\n" + self.overall_feed_tank_middle_ls.name + ": " + str(self.overall_feed_tank_middle_ls.current_value) + "\n")

            self.system.system_problem = "FEED_EMPTY"
            self.stop_server()
            return

        if self.overall_purge_tank_high_ls.current_value == "CLOSED":
            print("THE PURGE TANK IS FULL. PLEASE EMPTY IT. SHUTTING DOWN SYSTEM.")
            self.system.system_problem = "PURGE_FULL"
            self.stop_server()
            return

        if self.overall_rinse_tank_ls.current_value == "OPEN":
            print("LEAK IN THE RINSE TANK! PLEASE CHECK.")
            print("SHOWN ON LEVEL SWITCH " + self.overall_rinse_tank_ls.name + " #" + str(self.overall_rinse_tank_ls.id))
            self.stop_server()
            self.system.system_problem = "LOW_RINSE"
            return

        if self.overall_feed_tank_middle_ls.current_value == "OPEN":
            print("THE FEED TANK IS LESS THAN HALF FULL")
            self.system.warning_feed_low = True

        if self.overall_feed_tank_high_ls.current_value == "CLOSED":
            print("THE FEED TANK IS ALMOST FULL. MAKE SURE YOU DON'T FILL IT TOO MUCH.")
            self.system.warning_feed_high = True


        if self.overall_purge_tank_middle_ls.current_value == "CLOSED":
            print("THE PURGE TANK IS ALMOST FULL – PREPARE TO EMPTY IT.")
            self.system.warning_purge_high = True



    def stop_server(self):
        print("STOPPING CONTROL!")
        self.stop_control = True

        self.run_overall = False
        self.ed.run_ed = False
        self.uf.run_uf = False

        # Make sure we've left the control loops, lest we turn some instruments back on again.
        time.sleep(5)

        self.ed.turn_off_ed()
        self.uf.turn_off_uf()

        print("TURNED EVERYTHING OFF")

    def stop(self):
        self.overall_control_thread.join()


if __name__ == '__main__':
    pass
