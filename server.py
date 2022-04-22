import ArduinoCommunication as ard_com
import GUI.GUI as gui
from threading import Thread
import time
import sensors
import Sensor_Update_List as ulist

class Command_Center:

    command_sender_thread: Thread
    run = True

    def __init__(self, arduino, interface):
        self.voltage_1 = 0.0
        self.voltage_2 = 0.0
        self.arduino: ard_com.talktoArduino = arduino
        self.interface: gui.apason_GUIApp = interface

        self.command_sender_thread = Thread(target=self.run)
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

    def run(self):
        while (self.run):

            if(self.fetchVoltage()):
                self.arduino.sendVoltage(1, self.voltage_1, 'A')
                self.arduino.sendVoltage(1, self.voltage_2, 'B')


            time.sleep(1)

    def stop(self):
        self.command_sender_thread.join()


if __name__ == '__main__':

    arduino = ard_com.talktoArduino()

    sensors = sensors.Arduino_Sensors()

    update_list = ulist.Sensor_Update_List()

    index = 0

    for sensor in update_list.lst:
        sensor.updateValue(arduino.retrieveMeasurement(1, sensors.pressure_sensors[index]))
        index += 1

    for sensor in update_list.lst:
        print(sensor.current_value)