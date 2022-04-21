import talktoArduino as talk
import configurations as conf
import sensors as sens
import GUI.GUI as gui
from threading import Thread
import time


class GetVoltage:
    p:Thread
    def __init__(self):
        self.voltage_1 = 0
        self.voltage_2 = 0
        self.p = Thread(target=self.run)
        self.p.start()

    def fetchVoltage(self, interface):
        self.voltage_1 = interface.voltage_output_1
        self.voltage_2 = interface.voltage_output_2

    def run(self):
        while (True): #TODO: add condition to leave the while loop
            print(self.voltage_1)
            print(self.voltage_2)

            time.sleep(1)

    def stop(self):
        self.p.join()


if __name__ == '__main__':
    view: gui.apason_GUIApp = gui.apason_GUIApp()
    voltage = GetVoltage()
    view.setServer(voltage)
    view.run()
