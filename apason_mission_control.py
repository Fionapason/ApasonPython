import ArduinoCommunication as ard_com
import GUI.gui as gui
from threading import Thread
import time
import Arduino_Sensors
import Sensor_Update_List as ulist
import Arduino_Control_Instruments as ard_control_ins
import apason_system as system


class Command_Center:

    command_center_thread: Thread
    run_cc = True
    #
    # def __init__(self, arduino_com, arduino_control, pump_id_1, pump_id_2, interface):
    #     self.voltage_int_1 = 0.0
    #     self.voltage_int_2 = 0.0
    #     self.arduino_control: arduino_volt.Arduino_Control_Instruments() = arduino_control
    #
    #     self.pump_1 = self.arduino_control.pump_instruments[pump_id_1]
    #     self.pump_2 = self.arduino_control.pump_instruments[pump_id_2]
    #
    #     self.ard_com : ard_com.ArduinoCommunication() = arduino_com
    #     self.interface: gui.apason_GUIApp = interface
    #
    #     self.command_sender_thread = Thread(target=self.run)
    #     self.command_sender_thread.start()
    #
    #
    # def fetchVoltage(self):
    #     if ( (self.voltage_int_1 != self.interface.voltage_output_1)
    #          | (self.voltage_int_2 != self.interface.voltage_output_2)):
    #
    #         self.voltage_int_1 = self.interface.voltage_output_1
    #         self.voltage_int_2 = self.interface.voltage_output_2
    #
    #         return True
    #
    #     return False
    #
    #
    #
    #
    # def stop_server(self):
    #     self.run_cc = False
    #     #kill system
    #
    # def run(self):
    #     while (self.run_cc):
    #
    #         if(self.fetchVoltage()):
    #             new_volt_1 = self.pump_1.find_Voltage(self.voltage_int_1)
    #             self.ard_com.sendVoltage(new_volt_1, self.pump_1)
    #
    #             new_volt_2 = self.pump_2.find_Voltage(self.voltage_int_2)
    #             self.ard_com.sendVoltage(new_volt_2, self.pump_2)
    #         time.sleep(1)
    #
    #
    # def stop(self):
    #     self.command_sender_thread.join()
    def __init__(self, arduinos, ard_control, interface, update_list):
        self.ard_com : ard_com.ArduinoCommunication() = arduinos
        self.apason_system =  system.Apason_System()
        self.ard_control : ard_control_ins.Arduino_Control_Instruments() = ard_control
        self.apason_system.turn_on_system(update_list)
        self.interface = interface
        self.command_center_thread = Thread(target=self.run)
        self.command_center_thread.start()

    def send_commands(self):

        index = 0

        for pump in self.apason_system.system_pumps:
            if pump.changed:
                self.ard_com.sendVoltage(volt=self.ard_control.pump_instruments[index].find_Voltage(pump.state), control_instrument=self.ard_control.pump_instruments[pump.id])
                pump.changed = False
            index += 1

        index = 0
        for ocv_no in self.apason_system.system_ocvs_no:
            if ocv_no.changed:
                self.ard_com.setDigital(state=ocv_no.state, control_instrument=self.ard_control.ocv_normally_open_instruments[index])
                ocv_no.changed = False
            index += 1
        index = 0
        for ocv_nc in self.apason_system.system_ocvs_nc:
            if ocv_nc.changed:
                self.ard_com.setDigital(state=ocv_nc.state, control_instrument=self.ard_control.ocv_normally_closed_instruments[index])
                ocv_nc.changed = False
            index += 1

        index = 0
        for cv3 in self.apason_system.system_cv3s:
            if cv3.changed:
                self.ard_com.setDigital(state=cv3.state, control_instrument=self.ard_control.cv3_instruments[index])
                cv3.changed = False
            index += 1

        if self.apason_system.polarity.changed:
            self.ard_com.setDigital(state=self.apason_system.polarity.state, control_instrument=self.ard_control.polarity)
            self.apason_system.polarity.changed = False

    #TODO check GUI buttons for on/off

    def run(self):


        while(self.run_cc):
            self.send_commands()
            time.sleep(0.1)

    def stop_server(self):
        self.run_cc = False
        self.apason_system.turn_off_system()
        self.set_zero()
        self.send_commands()

    def set_zero(self):
        for pump in self.apason_system.system_pumps:
            if pump.state != 0.0:
                pump.set_new_state(new_state=0.0)
        for ocv_no in self.apason_system.system_ocvs_no:
            if ocv_no.state != "LOW":
                ocv_no.set_new_state(new_state="LOW")
        for ocv_nc in self.apason_system.system_ocvs_nc:
            if ocv_nc.state != "LOW":
                ocv_nc.set_new_state(new_state="LOW")
        for cv3 in self.apason_system.system_cv3s:
            if cv3.state != "LOW":
                cv3.set_new_state(new_state="LOW")
        self.apason_system.polarity.set_new_state(new_state="OFF")


# TODO finish Update_List

class Update_List:

    update_list_thread: Thread
    run_ul = True

    def __init__(self, interface, list, arduino):
        self.interface: gui.apason_GUIApp = interface
        self.list = list
        self.arduino = arduino
        self.last_print = time.time()

        self.update_list_thread = Thread(target=self.run_update_list)
        self.update_list_thread.start()


    def set_from_list(self):

        self.interface.pressure_display_1 = str(self.list.pressure[0].current_value)
        # self.interface.pressure_display_2 = str(self.list.pressure[1].current_value)
        # self.interface.pressure_display_3 = str(self.list.pressure[2].current_value)
        #
        # self.interface.massflow_display_1 = str(self.list.massflow[0].current_value)
        # self.interface.massflow_display_2 = str(self.list.massflow[1].current_value)
        # self.interface.massflow_display_3 = str(self.list.massflow[2].current_value)

        # print("Diluate Out Conductivity: " + str(self.list.conductivity[1].current_value) + "\n")

        # print("UF HIGH LEVEL SWITCH READING: " + self.list.levelswitch[0].current_value)
        # print("UF MIDDLE LEVEL SWITCH READING: " + self.list.levelswitch[1].current_value)
        # print("\n--------- CURRENT MASSFLOWS:")

        if time.time() - self.last_print > 20.0:
            print("UF FEED FLOW: " + str(self.list.massflow[1].current_value))

        #
        # if time.time() - self.last_print > 30.0:
        #     print("---------")
        #     print("CURRENT CONDUCTIVITY \n DILUATE OUT: " + str(self.list.conductivity[1].current_value) + "\n")
        #     print("CURRENT CONDUCTIVITY \n CONCENTRATE: " + str(self.list.conductivity[2].current_value) + "\n")
        #     print("---------")

    def run_update_list(self):
        while (self.run_ul):

            index = 0

            for sensor in self.list.pressure:
                sensor.updateValue(self.arduino.retrieveMeasurement(sensors.pressure_sensors[index]))
                index += 1

            index = 0

            for sensor in self.list.levelswitch:
                # print("Checking Level Switch: " + sensor.name)
                digital_1 = self.arduino.checkDigital(sensors.levelswitch_sensors[index])
                digital_2 = self.arduino.checkDigital(sensors.levelswitch_sensors[index])
                digital_3 = self.arduino.checkDigital(sensors.levelswitch_sensors[index])
                if (digital_1 == digital_2) & (digital_2 == digital_3):
                    sensor.updateValue(digital_1)
                index += 1

            index = 0

            for sensor in self.list.massflow:
                sensor.updateValue(self.arduino.retrieveMeasurement(sensors.massflow_sensors[index]))
                index += 1

            index = 0
            for sensor in self.list.conductivity:
                sensor.updateValue(self.arduino.retrieveMeasurement(sensors.conductivity_sensors[index]))
                index += 1
            self.set_from_list()
            time.sleep(0.5)


    def stop_server(self):
        self.run_ul = False

    def stop(self):
        self.update_list_thread.join()


if __name__ == '__main__':


    arduinos = ard_com.ArduinoCommunication()

    sensors = Arduino_Sensors.Arduino_Sensors()

    control_instruments = ard_control_ins.Arduino_Control_Instruments()

    update_list = ulist.Sensor_Update_List()

    # arduinos.sendVoltage(volt=0, control_instrument=control_instruments.pump_instruments[4])
    # arduinos.sendVoltage(volt=900, control_instrument=control_instruments.pump_instruments[5])
    # arduinos.sendVoltage(volt=0, control_instrument=control_instruments.pump_instruments[6])
    # arduinos.sendVoltage(volt=0, control_instrument=control_instruments.pump_instruments[7])

    view: gui.apason_GUIApp = gui.apason_GUIApp()

    update = Update_List(interface=view,
                         list=update_list,
                         arduino=arduinos)

    command_center = Command_Center(arduinos=arduinos,
                                    ard_control=control_instruments,
                                    update_list=update_list,
                                    interface=view)

    view.setServer(command_center, update)

    view.run()
