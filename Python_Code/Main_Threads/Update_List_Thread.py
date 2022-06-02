import time
from threading import Thread

from Main_Threads.GUI import gui as gui

"""
This thread regularly measures all the sensors current values, using Arduino_Sensors and Arduino_Utilities,
and saves these values in an instance of the Sensor_Update_List class.

The thread also sets the values that need to be shown on the interface and formats them in an easy to read way.
"""

class Update_List:

    update_list_thread: Thread
    run_ul = True

    def __init__(self, interface, list, arduino, arduino_sensors):
        self.interface: gui.apason_GUIApp = interface
        self.list = list
        self.arduino = arduino
        self.sensors = arduino_sensors
        self.last_print = time.time()
        self.measurements_loops = 0
        self.start_control = False

        self.update_list_thread = Thread(target=self.run_update_list)
        self.update_list_thread.start()


    def set_from_list(self):

        # self.interface.pressure_display_1 = str(self.list.pressure[0].current_value)

        output_flow_number = round(self.list.massflow[5].current_value, 2)
        diluate_in_number = round(self.list.conductivity[2].current_value, 2)
        diluate_out_number = round(self.list.conductivity[0].current_value, 2)

        if output_flow_number < 0.0:
            output_flow_number = 0.0
        if diluate_in_number < 0.0:
            diluate_in_number = 0.0
        if diluate_out_number < 0.0:
            diluate_out_number = 0.0

        diluate_in = str(diluate_in_number) + " " + self.list.conductivity[2].unit
        diluate_out = str(diluate_out_number) + " " + self.list.conductivity[0].unit
        output_flow = str(output_flow_number) + " " + self.list.massflow[5].unit

        self.interface.diluate_in_display = diluate_in
        self.interface.diluate_out_display = diluate_out
        self.interface.output_flow_display = output_flow


    def run_update_list(self):
        while (self.run_ul):

            index = 0

            for sensor in self.list.pressure:
                sensor.update_value(self.arduino.retrieve_measurement(self.sensors.pressure_sensors[index]))
                index += 1

            index = 0

            for sensor in self.list.massflow:
                sensor.update_value(self.arduino.retrieve_measurement(self.sensors.massflow_sensors[index]))
                index += 1


            index = 0

            for sensor in self.list.levelswitch:
                digital_1 = self.arduino.check_digital(self.sensors.levelswitch_sensors[index])
                sensor.update_value(digital_1)
                index += 1


            index = 0

            for sensor in self.list.massflow:
                sensor.update_value(self.arduino.retrieve_measurement(self.sensors.massflow_sensors[index]))
                index += 1


            index = 0
            for sensor in self.list.conductivity:
                sensor.update_value(self.arduino.retrieve_measurement(self.sensors.conductivity_sensors[index]))
                index += 1

            index = 0

            for sensor in self.list.massflow:
                sensor.update_value(self.arduino.retrieve_measurement(self.sensors.massflow_sensors[index]))
                index += 1

            self.set_from_list()

            self.measurements_loops += 1



    def stop_server(self):
        self.run_ul = False

    def stop(self):
        self.update_list_thread.join()
