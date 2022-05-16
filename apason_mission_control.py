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

        for pump in self.apason_system.system_pumps:
            if pump.changed:
                self.ard_com.sendVoltage(volt=self.ard_control.pump_instruments[pump.id].find_Voltage(pump.state), control_instrument=self.ard_control.pump_instruments[pump.id])
                pump.changed = False

        for ocv_no in self.apason_system.system_ocvs_no:
            if ocv_no.changed:
                self.ard_com.setDigital(state=ocv_no.state, control_instrument=self.ard_control.ocv_normally_open_instruments[ocv_no.id])
                ocv_no.changed = False

        for ocv_nc in self.apason_system.system_ocvs_nc:
            if ocv_nc.changed:
                self.ard_com.setDigital(state=ocv_nc.state, control_instrument=self.ard_control.ocv_normally_closed_instruments[ocv_nc.id])
                ocv_nc.changed = False

        for cv3 in self.apason_system.system_cv3s:
            if cv3.changed:
                self.ard_com.setDigital(state=cv3.state, control_instrument=self.ard_control.cv3_instruments[cv3.id])
                cv3.changed = False

        if self.apason_system.polarity.changed:
            self.ard_com.setDigital(state=self.apason_system.polarity.state, control_instrument=self.ard_control.polarity)
            self.apason_system.polarity.changed = False

    #TODO check GUI buttons for on/off

    def run(self):


        while(self.run_cc):
            self.send_commands()
            time.sleep(1)

    def stop_server(self):
        self.run_cc = False
        self.set_zero()
        self.send_commands()
        self.apason_system.turn_off_system()

    def set_zero(self):
        for pump in self.apason_system.system_pumps:
            pump.set_new_state(new_state=0.0)
        for ocv_no in self.apason_system.system_ocvs_no:
            ocv_no.set_new_state(new_state="LOW")
        for ocv_nc in self.apason_system.system_ocvs_nc:
            ocv_nc.set_new_state(new_state="LOW")
        for cv3 in self.apason_system.system_cv3s:
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

        print("UF Feed Current Massflow: " + str(self.list.massflow[0].current_value) + "\n")
        print("UF Backwash Current Massflow: " + str(self.list.massflow[1].current_value) + "\n")

        # print("UF HIGH LEVEL SWITCH READING: " + self.list.levelswitch[0].current_value)
        # print("UF MIDDLE LEVEL SWITCH READING: " + self.list.levelswitch[1].current_value)


    def run_update_list(self):
        while (self.run_ul):
            index = 0

            for sensor in self.list.pressure:
                sensor.updateValue(self.arduino.retrieveMeasurement(sensors.pressure_sensors[index]))
                index += 1

            index = 0

            for sensor in self.list.levelswitch:
                digital = self.arduino.checkDigital(sensors.levelswitch_sensors[index])
                sensor.updateValue(digital)
                index += 1

            index = 0

            for sensor in self.list.massflow:
                sensor.updateValue(self.arduino.retrieveMeasurement(sensors.massflow_sensors[index]))
                index += 1

            self.set_from_list()
            time.sleep(5)


    def stop_server(self):
        self.run_ul = False

    def stop(self):
        self.update_list_thread.join()


if __name__ == '__main__':


    arduinos = ard_com.ArduinoCommunication()

    sensors = Arduino_Sensors.Arduino_Sensors()

    control_instruments = ard_control_ins.Arduino_Control_Instruments()

    update_list = ulist.Sensor_Update_List()

    arduinos.sendVoltage(volt=0, control_instrument=control_instruments.pump_instruments[0])
    arduinos.sendVoltage(volt=820, control_instrument=control_instruments.pump_instruments[2])
    arduinos.sendVoltage(volt=0, control_instrument=control_instruments.pump_instruments[1])
    arduinos.sendVoltage(volt=575, control_instrument=control_instruments.pump_instruments[3])

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
