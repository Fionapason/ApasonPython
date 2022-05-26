from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty #, NumericProperty
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

#TODO make warning messages

class GUI_GridLayout(GridLayout):

    system_on = False
    post_treatment_off = False

    diluate_in_label = StringProperty("Pre-ED Conductivity:")
    diluate_out_label = StringProperty("Post-ED Conductivity:")
    output_flow_label = StringProperty("Current Output Volume:")

    on_off_label = StringProperty("SYSTEM")
    pt_label = StringProperty("OUTPUT PUMP")

    diluate_in_display = StringProperty()
    diluate_out_display = StringProperty()
    output_flow_display = StringProperty()

    def on_off_switch_callback(self, switchObject, switchValue, pt_switch):
        if switchValue:
            self.switch_system_on(pt_switch)
        else:
            self.switch_system_off(pt_switch)

    def pt_switch_callback(self, switchObject, switchValue):
        if switchValue:
            self.post_treatment_off = False
            print("POST TREATMENT ON!")
        else:
            self.post_treatment_off = True
            print("POST TREATMENT OFF!")

    def enable_pt(self, pt_switch):
        pt_switch.disabled = False

    def disable_pt(self, pt_switch):
        pt_switch.disabled = True

    def switch_system_on(self, pt_switch):
        print("SYSTEM ON SWITCH ENGAGED!")
        self.system_on = True
        self.enable_pt(pt_switch)

    def switch_system_off(self, pt_switch):
        print("SYSTEM OFF SWITCH ENGAGED!")
        self.system_on = False
        self.disable_pt(pt_switch)

    def popup_feed_low(self):
        show = Popup_Window_Feed_Low()
        self.popup_feed_low_window = Popup(title="Feed Tank Getting Empty",
                                           content=show,
                                           size_hint=(0.5, 0.5))
        self.popup_feed_low_window.open()

    def popup_purge_high(self):
        show = Popup_Window_Purge_High()
        self.popup_purge_high_window = Popup(title="Purge Tank Almost Full",
                                            content=show,
                                            size_hint=(0.5, 0.5))
        self.popup_purge_high_window.open()

    def popup_feed_high(self):
        show = Popup_Window_Feed_High()
        self.popup_feed_high_window = Popup(title="Feed Tank Almost Full",
                                            content=show,
                                            size_hint=(0.5, 0.5))
        self.popup_feed_high_window.open()

    def build(self):

        self.switch_system_on_off = Switch(active=False)
        self.switch_system_on_off.bind(active=self.on_off_switch_callback)
        self.add_widget(self.switch_system_on_off)

        self.switch_pt_on_off = Switch(active=True, disabled=True)
        self.switch_pt_on_off.bind(active=self.pt_switch_callback)
        self.add_widget(self.switch_pt_on_off)



        self.add_widget(Label(text=self.diluate_in_label))
        self.add_widget(Label(text=self.diluate_in_display))

        self.add_widget(Label(text=self.diluate_out_label))
        self.add_widget(Label(text=self.diluate_out_display))

        self.add_widget(Label(text=self.output_flow_label))
        self.add_widget(Label(text=self.output_flow_display))

        self.add_widget(Label(text=self.pt_label))
        self.add_widget(Label(text=self.on_off_label))

class Popup_Window_Feed_High(FloatLayout):

    high_feed_warning = StringProperty("The water level in the feed tank is very high. \n Make sure you don't overflow!")

    def build(self):
        self.add_widget(Label(text=self.high_feed_warning))

class Popup_Window_Feed_Low(FloatLayout):

    low_feed_warning = StringProperty("The water level in the feed tank is getting low. \n If you don't refill soon, the system will turn off.")

    def build(self):
        self.add_widget(Label(text=self.low_feed_warning))

class Popup_Window_Purge_High(FloatLayout):

    high_purge_warning = StringProperty("The water level in the purge tank is getting high. \n If you don't empty it soon, the system will turn off.")

    def build(self):
        self.add_widget(Label(text=self.high_purge_warning))

class apason_GUIApp(App):

    system_on = False
    system_turned_on = False

    post_treatment_off = False
    post_treatment_turned_off = False

    diluate_in_display = StringProperty()
    diluate_out_display = StringProperty()
    output_flow_display = StringProperty()

    popup_feed_high_now = False
    popup_feed_low_now = False
    popup_purge_high_now = False


    def update_switches(self, dt):

        if not self.system_turned_on:

            if self.layout.system_on:
                print("SENDING BUTTON MESSAGE ON!")
                self.command_center.system_on = True
                self.system_turned_on = True
        else:
            if not self.layout.system_on:
                self.command_center.system_on = False
                self.system_turned_on = False

        if not self.post_treatment_turned_off:
            if self.layout.post_treatment_off:
                self.command_center.post_treatment_off = True
                self.post_treatment_turned_off = True
        else:
            if not self.layout.post_treatment_off:
                self.command_center.post_treatment_off = False
                self.post_treatment_turned_off = False


    def update_inputs(self, dt):
        self.layout.diluate_in_display = self.diluate_in_display
        self.layout.diluate_out_display = self.diluate_out_display
        self.layout.output_flow_display = self.output_flow_display

    def check_warnings(self, dt):
        if self.popup_feed_high_now:
            self.layout.popup_feed_high()
            self.popup_feed_high_now = False
        if self.popup_feed_low_now:
            self.layout.popup_feed_low()
            self.popup_feed_low_now = False
        if self.popup_purge_high_now:
            self.layout.popup_purge_high()
            self.popup_purge_high_now = False


    def setServer(self, command_center, update_list):
        self.command_center = command_center
        self.update_list = update_list

    def build(self):
        self.layout = GUI_GridLayout()
        Clock.schedule_interval(self.update_switches, 1.0)
        Clock.schedule_interval(self.update_inputs, 1.0)
        Clock.schedule_interval(self.check_warnings, 1.0)
        return self.layout

    def on_stop(self):
        print("APP CLOSED. SHUTTING DOWN…")
        self.command_center.stop_server()
        self.update_list.stop_server()


if __name__ == '__main__':
    apason_GUIApp().run()
