import ArduinoCommunication as ard_com
import GUI.GUI as gui
from threading import Thread, Lock
import time
import Arduino_Sensors
import Sensor_Update_List as ulist
import Arduino_Control_Instruments as arduino_volt

#TODO make better for control

class Command_Center:

    command_sender_thread: Thread
    run_cc = True

    def __init__(self, arduino_com, arduino_control, interface, pump_id, lock):
        self.voltage_int_1 = 0.0
        self.voltage_int_2 = 0.0
        self.arduino_control: arduino_volt.Arduino_Control_Instruments() = arduino_control
        self.pump = self.arduino_control.pump_instruments[pump_id]
        self.ard_com : ard_com.ArduinoCommunication() = arduino_com
        self.interface: gui.apason_GUIApp = interface

        self.command_sender_thread = Thread(target=self.run, args=(lock,))
        self.command_sender_thread.start()


    def fetchVoltage(self):
        if ( (self.voltage_int_1 != self.interface.voltage_output_1)
             | (self.voltage_int_2 != self.interface.voltage_output_2)):

            self.voltage_int_1 = self.interface.voltage_output_1
            self.voltage_int_2 = self.interface.voltage_output_2

            return True

        return False

    def stop_server(self):
        self.run_cc = False

    def run(self, lock):
        while (self.run_cc):

            if(self.fetchVoltage()):
                new_volt = self.pump.find_Voltage(self.voltage_int_1)
                self.ard_com.sendVoltage(new_volt, self.pump , lock)
            time.sleep(1)


    def stop(self):
        self.command_sender_thread.join()

class Update_List:

    update_list_thread: Thread
    run_ul = True

    def __init__(self, interface, list, arduino, lock):
        self.interface: gui.apason_GUIApp = interface
        self.list = list
        self.arduino = arduino

        self.update_list_thread = Thread(target=self.run, args=(lock,))
        self.update_list_thread.start()

    def set_from_list(self):

        self.interface.pressure_display_1 = str(self.list.pressure[0].current_value)
        # self.interface.pressure_display_2 = str(self.list.pressure[1].current_value)
        # self.interface.pressure_display_3 = str(self.list.pressure[2].current_value)
        #
        # self.interface.massflow_display_1 = str(self.list.massflow[0].current_value)
        # self.interface.massflow_display_2 = str(self.list.massflow[1].current_value)
        # self.interface.massflow_display_3 = str(self.list.massflow[2].current_value)



    def run(self, lock):
        while (self.run_ul):
            index = 0
            for sensor in self.list.pressure:
                sensor.updateValue(self.arduino.retrieveMeasurement(sensors.pressure_sensors[index], lock))
                index += 1

            index = 0

            for sensor in self.list.massflow:
                sensor.updateValue(self.arduino.retrieveMeasurement(sensors.massflow_sensors[index], lock))
                index += 1

            self.set_from_list()
            time.sleep(1)

    def stop_server(self):
        self.run_ul = False

    def stop(self):
        self.update_list_thread.join()


if __name__ == '__main__':

    arduino_lock = Lock()

    arduinos = ard_com.ArduinoCommunication()

    sensors = Arduino_Sensors.Arduino_Sensors()

    control_instruments = arduino_volt.Arduino_Control_Instruments()

    update_list = ulist.Sensor_Update_List()

    view: gui.apason_GUIApp = gui.apason_GUIApp()

    voltage = Command_Center(arduino_com=arduinos,
                             arduino_control=control_instruments,
                             interface=view,
                             pump_id=0,
                             lock=arduino_lock)

    pressure = Update_List(interface=view,
                           list=update_list,
                           arduino=arduinos,
                           lock=arduino_lock)

    view.setServer(voltage, pressure)
    view.run()