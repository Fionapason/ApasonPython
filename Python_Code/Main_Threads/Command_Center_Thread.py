import time
from threading import Thread

from Arduino_Communication import Arduino_Control_Instruments as ard_control_ins, \
    Arduino_Utilities as ard_com
from Sensor_Instrument_Tracking import Apason_System_Instruments as system

"""
This thread checks the states of the instrument objects, which are kept in an instance of the Apason_System class,
and sends the according commands found in the Arduino_Control_Instruments class via the Arduino_Utilities functions on
to the Arduino to be effectively carried out.

It also initializes the Control thread and carries warning and problem messages from the control system over to the GUI thread,
so that they may be displayed there. Vice Versa, if the GUI switches have been engaged, the Command Center also forwards this
information to the Control System and stops it, if necessary.
"""

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
        self.ard_com : ard_com.Arduino_Utilities() = arduinos
        self.apason_system =  system.Apason_System()
        self.ard_control : ard_control_ins.Arduino_Control_Instruments() = ard_control
        self.interface = interface
        self.list = update_list
        self.command_center_thread = Thread(target=self.run)
        self.command_center_thread.start()

    def send_commands(self):

        # Iterating through all instruments in apason_system and, if they have been changed, sending the appropriate command to the Arduino

        index = 0

        for pump in self.apason_system.system_pumps:
            if pump.changed:
                self.ard_com.send_voltage(volt=self.ard_control.pump_instruments[index].find_voltage(pump.state), control_instrument=self.ard_control.pump_instruments[index])
                pump.changed = False
            index += 1


        index = 0
        for ocv_no in self.apason_system.system_ocvs_no:
            if ocv_no.changed:
                self.ard_com.set_digital(state=ocv_no.state, control_instrument=self.ard_control.ocv_normally_open_instruments[index])
                ocv_no.changed = False
            index += 1


        index = 0
        for ocv_nc in self.apason_system.system_ocvs_nc:
            if ocv_nc.changed:
                self.ard_com.set_digital(state=ocv_nc.state, control_instrument=self.ard_control.ocv_normally_closed_instruments[index])
                ocv_nc.changed = False
            index += 1


        index = 0
        for cv3 in self.apason_system.system_cv3s:
            if cv3.changed:
                self.ard_com.set_digital(state=cv3.state, control_instrument=self.ard_control.cv3_instruments[index])
                cv3.changed = False
            index += 1


        if self.apason_system.polarity.changed:
            self.ard_com.set_digital(state=self.apason_system.polarity.state, control_instrument=self.ard_control.polarity)
            self.apason_system.polarity.changed = False


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
                self.set_problem()
                self.send_commands()
                time.sleep(1.5)



            time.sleep(3)

    def check_warnings(self):

        # Check for all possible warnings.
        # If the warning has already been shown but 20 seconds have not yet passed, do not show it again yet.

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
                self.interface.popup_purge_high_now = True
                print("PURGE HIGH")
            else:
                elapsed_time = time.time() - self.warning_purge_high_timer
                print(elapsed_time)
                if elapsed_time > 20.0:
                    print("PURGE WARNING: 20 SECONDS HAVE PASSED. ANOTHER WARNING.")
                    self.warning_purge_high_timer_started = False

    def set_problem(self):

        # Problems mean system shut down. Thus, only one problem "needs" to exist at a time.

        self.interface.problem = self.apason_system.system_problem


    def start_system(self):
        self.apason_system.turn_on_system(list=self.list)

    def stop_system(self):
        self.system_on = False
        self.apason_system.turn_off_system()
        # To ascertain a safe shutdown, we send a low command to every single instrument before we stop the system.
        self.set_zero()
        self.send_commands()

    def stop_server(self):

        # This is when the GUI window has been closed and we are ending the programme completely. All threads need to be ended properly.

        print("I'm Trying To Stop The Command Center Server")
        self.apason_system.turn_off_system()
        self.system_on = False
        self.run_cc = False
        self.set_zero()
        self.send_commands()

    def stop(self):
        self.command_center_thread.join()


    def set_zero(self):
        # Changing the state of all instruments to a low power.
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
