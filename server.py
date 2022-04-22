import ArduinoCommunication as ard_com
import configurations as conf
import sensors as sens
import GUI.GUI as gui
from threading import Thread
import time


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
    #
    # arduino = ard_com.talktoArduino()

    sensors = conf.sensor_configurations["massflow"]
    sensor = sensors[0]

    print(sensor["name"])


    # view: gui.apason_GUIApp = gui.apason_GUIApp()
    # voltage = Command_Center(arduino, view)
    # view.setServer(voltage)
    # view.run()
