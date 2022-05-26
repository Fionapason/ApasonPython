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
    system_on = False
    system_turned_on = False
    post_treatment_off = False
    post_treatment_turned_off = False

    warning_feed_high_timer_started = False
    warning_purge_high_timer_started = False
    warning_feed_low_timer_started = False

    def __init__(self, arduinos, ard_control, interface, update_list):
        self.ard_com : ard_com.ArduinoCommunication() = arduinos
        self.apason_system =  system.Apason_System()
        self.ard_control : ard_control_ins.Arduino_Control_Instruments() = ard_control
        self.interface = interface
        self.list = update_list
        self.command_center_thread = Thread(target=self.run)
        self.command_center_thread.start()

    def send_commands(self):

        index = 0

        for pump in self.apason_system.system_pumps:
            if pump.changed:
                self.ard_com.sendVoltage(volt=self.ard_control.pump_instruments[index].find_Voltage(pump.state), control_instrument=self.ard_control.pump_instruments[index])
                pump.changed = False
                time.sleep(0.2)
            index += 1


        index = 0
        for ocv_no in self.apason_system.system_ocvs_no:
            if ocv_no.changed:
                self.ard_com.setDigital(state=ocv_no.state, control_instrument=self.ard_control.ocv_normally_open_instruments[index])
                ocv_no.changed = False
                time.sleep(0.2)
            index += 1


        index = 0
        for ocv_nc in self.apason_system.system_ocvs_nc:
            if ocv_nc.changed:
                self.ard_com.setDigital(state=ocv_nc.state, control_instrument=self.ard_control.ocv_normally_closed_instruments[index])
                ocv_nc.changed = False
                time.sleep(0.2)
            index += 1


        index = 0
        for cv3 in self.apason_system.system_cv3s:
            if cv3.changed:
                self.ard_com.setDigital(state=cv3.state, control_instrument=self.ard_control.cv3_instruments[index])
                cv3.changed = False
                time.sleep(0.2)
            index += 1


        if self.apason_system.polarity.changed:
            self.ard_com.setDigital(state=self.apason_system.polarity.state, control_instrument=self.ard_control.polarity)
            self.apason_system.polarity.changed = False
            time.sleep(0.2)

    #TODO check GUI buttons for on/off

    def post_treatment_pump(self):

        if not self.post_treatment_turned_off:

            if self.post_treatment_off:
                print("COMMAND CENTER: POST TREATMENT TURNED OFF")
                self.apason_system.overall_control.ed.post_treatment_switch_off = True
                self.post_treatment_turned_off = True

        else:

            if not self.post_treatment_off:
                print("COMMAND CENTER: POST TREATMENT TURNED ON")
                self.apason_system.overall_control.ed.post_treatment_switch_off = False
                self.post_treatment_turned_off = False

    def run(self):

        while (self.run_cc):

            print("SYSTEM TURNED ON: " + str(self.system_on))

            if not self.system_turned_on:
                print("SYSTEM CURRENTLY OFF. CHECKING IF IT SHOULD BE TURNED ON.")
                if self.system_on:
                    self.start_system()
                    self.system_turned_on = True
            else:
                print("SYSTEM CURRENTLY ON. CHECKING IF IT SHOULD BE TURNED OFF.")
                if self.apason_system.overall_control.stop_control:
                    self.apason_system.turn_off_system()
                    self.system_turned_on = False
                    self.system_on = False
                if not self.system_on:
                    self.apason_system.turn_off_system()
                    self.system_turned_on = False

            while (self.system_on):
                self.post_treatment_pump()
                self.check_warnings()
                self.send_commands()
                time.sleep(1)

            if self.apason_system.system_problem:
                print(self.apason_system.system_problem)


            time.sleep(3)

    def check_warnings(self):

        print("CHECKING WARNINGS...")

        if self.apason_system.warning_feed_high:
            if not self.warning_feed_high_timer_started:
                self.warning_feed_high_timer = time.time()
                self.warning_feed_high_timer_started = True
                self.interface.popup_feed_high_now = True
                print("FEED HIGH!")
            else:
                elapsed_time = time.time() - self.warning_feed_high_timer
                print(elapsed_time)
                if elapsed_time > 20.0:
                    print("FEED HIGH WARNING: 20 SECONDS HAVE PASSED. ANOTHER WARNING.")
                    self.warning_feed_high_timer_started = False
        if self.apason_system.warning_feed_low:
            if not self.warning_feed_low_timer_started:
                self.warning_feed_low_timer = time.time()
                self.warning_feed_low_timer_started = True
                self.interface.popup_feed_low_now = True
                print("FEED LOW!")
            else:
                elapsed_time = time.time() - self.warning_feed_low_timer
                print(elapsed_time)
                if elapsed_time > 20.0:
                    print("FEED LOW WARNING: 20 SECONDS HAVE PASSED. ANOTHER WARNING.")
                    self.warning_feed_low_timer_started = False

        if self.apason_system.warning_purge_high:
            if not self.warning_purge_high_timer_started:
                self.warning_purge_high_timer = time.time()
                self.warning_purge_high_timer_started = True
                # TODO POPUP
                self.interface.popup_purge_high_now = True
                print("PURGE HIGH")
            else:
                print(elapsed_time)
                elapsed_time = time.time() - self.warning_purge_high_timer
                if elapsed_time > 20.0:
                    print("PURGE WARNING: 20 SECONDS HAVE PASSED. ANOTHER WARNING.")
                    self.warning_purge_high_timer_started = False


    def start_system(self):
        self.apason_system.turn_on_system(list=self.list)

    def stop_system(self):
        self.system_on = False
        self.apason_system.turn_off_system()
        self.set_zero()
        self.send_commands()

    def stop_server(self):
        print("I'm Trying To Stop The Command Center Server")
        self.apason_system.turn_off_system()
        self.system_on = False
        self.run_cc = False
        self.set_zero()
        self.send_commands()

    def stop(self):
        self.command_center_thread.join()


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
        self.measurements_loops = 0
        self.start_control = False

        self.update_list_thread = Thread(target=self.run_update_list)
        self.update_list_thread.start()


    def set_from_list(self):

        # self.interface.pressure_display_1 = str(self.list.pressure[0].current_value)

        output_flow_number = round(self.list.massflow[5].current_value, 2)  # TODO double check correct flow

        if output_flow_number < 0.0:
            output_flow_number = 0

        diluate_in = str(round(self.list.conductivity[2].current_value,2)) + " " + self.list.conductivity[2].unit
        diluate_out = str(round(self.list.conductivity[0].current_value,2)) + " " + self.list.conductivity[0].unit
        output_flow = str(output_flow_number) + " " + self.list.massflow[5].unit

        self.interface.diluate_in_display = diluate_in
        self.interface.diluate_out_display = diluate_out
        self.interface.output_flow_display = output_flow


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

            # for flow in self.list.massflow:
                # print(flow.name + " CURRENT FLOW: " + str(flow.current_value))

            self.set_from_list()

            self.measurements_loops += 1



    def stop_server(self):
        self.run_ul = False

    def stop(self):
        self.update_list_thread.join()


if __name__ == '__main__':


    arduinos = ard_com.ArduinoCommunication()

    sensors = Arduino_Sensors.Arduino_Sensors()

    control_instruments = ard_control_ins.Arduino_Control_Instruments()

    update_list = ulist.Sensor_Update_List()

    interface: gui.apason_GUIApp = gui.apason_GUIApp()

    update = Update_List(interface=interface,
                         list=update_list,
                         arduino=arduinos)



    command_center = Command_Center(arduinos=arduinos,
                                    ard_control=control_instruments,
                                    update_list=update_list,
                                    interface=interface)

    interface.setServer(command_center, update)

    interface.run()
