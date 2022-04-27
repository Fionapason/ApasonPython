import ArduinoCommunication as ard_com
import GUI.GUI as gui
from threading import Thread, Lock
import time
import sensors
import Sensor_Update_List as ulist

# TODO differentiate both run function names!

class Command_Center:

    command_sender_thread: Thread
    run = True

    def __init__(self, arduino, interface, lock):
        self.voltage_1 = 0.0
        self.voltage_2 = 0.0
        self.arduino: ard_com.ArduinoCommunication = arduino
        self.interface: gui.apason_GUIApp = interface

        self.command_sender_thread = Thread(target=self.run, args=(lock,))
        self.command_sender_thread.start()


    def fetchVoltage(self):
        if ( (self.voltage_1 != self.interface.voltage_output_1)
                | (self.voltage_2 != self.interface.voltage_output_2) ):
            self.voltage_1 = self.interface.voltage_output_1
            self.voltage_2 = self.interface.voltage_output_2
            return True

        return False

    def stop_server(self):
        self.run = False

    def run(self, lock):
        while (self.run):
            lock.acquire()
            if(self.fetchVoltage()):
                self.arduino.sendVoltage(1, self.voltage_1, 'A')
                self.arduino.sendVoltage(1, self.voltage_2, 'B')
            lock.release()
            time.sleep(1)


    def stop(self):
        self.command_sender_thread.join()

class Update_List:

    update_list_thread: Thread
    run = True

    def __init__(self, interface, lock):
        self.interface: gui.apason_GUIApp = interface
        self.list = ulist.Sensor_Update_List()

        self.update_list_thread = Thread(target=self.run, args=(lock,))
        self.update_list_thread.start()

    def set_from_list(self):
        self.interface.pressure_display_1 = str(self.list.pressure[0].current_value)


    def run(self, lock):
        while (self.run):
            lock.acquire()
            self.list.pressure[0].updateValue(arduino.retrieveMeasurement(1, sensors.pressure_sensors[0]))

            #if not len(self.list.pressure) == 0:
            self.set_from_list()
            lock.release()
            time.sleep(1)

    def stop_server(self):
        self.run = False

    def stop(self):
        self.update_list_thread.join()


if __name__ == '__main__':

    arduino_lock = Lock()

    arduino = ard_com.ArduinoCommunication()

    sensors = sensors.Arduino_Sensors()

    update_list = ulist.Sensor_Update_List()

    view: gui.apason_GUIApp = gui.apason_GUIApp()
    voltage = Command_Center(arduino, view, arduino_lock)
    pressure = Update_List(view, arduino_lock)
    view.setServer(voltage, pressure)
    view.run()