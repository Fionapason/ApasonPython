from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.button import Button
from kivy.clock import Clock

#TODO pick out actually visible values
#TODO make needed buttons
#TODO make warning messages

class GUI_GridLayout(GridLayout):

    system_on = False

    diluate_in_label = StringProperty("Diluate In Conductivity:")
    diluate_out_label = StringProperty("Diluate Out Conductivity:")
    output_flow_label = StringProperty("Current Output:")

    diluate_in_display = StringProperty()
    diluate_out_display = StringProperty()
    output_flow_display = StringProperty()

    system_on_button_label = StringProperty("TURN ON")
    system_off_button_label = StringProperty("TURN OFF")

    # TODO BUTTONS
    def press_system_on(self):
        print("SYSTEM ON BUTTON ENGAGED!")
        self.system_on = True

    def press_system_off(self):
        print("SYSTEM OFF BUTTON ENGAGED!")
        self.system_on = False

    def build(self):
        # self.add_widget(Label(text=self.voltage_label_1))
        # self.add_widget(self.voltage_input_1)
        #
        # self.add_widget(Label(text=self.voltage_label_2))
        # self.add_widget(self.voltage_input_2)

        self.submit_button_1 = Button(text=self.system_on_button_label)
        self.submit_button_1.bind(on_press=self.press_system_on)
        self.add_widget(self.submit_button_1)

        self.submit_button_2 = Button(text=self.system_off_button_label)
        self.submit_button_2.bind(on_press=self.press_system_off)
        self.add_widget(self.submit_button_2)

        self.add_widget(Label(text=self.diluate_in_label))
        self.add_widget(Label(text=self.diluate_in_display))

        self.add_widget(Label(text=self.diluate_out_label))
        self.add_widget(Label(text=self.diluate_out_display))

        self.add_widget(Label(text=self.output_flow_label))
        self.add_widget(Label(text=self.output_flow_display))



class apason_GUIApp(App):

    system_on = False
    system_turned_on = False
    system_turned_off = False

    diluate_in_display = StringProperty()
    diluate_out_display = StringProperty()
    output_flow_display = StringProperty()

    def update_buttons(self, dt):

        if not self.system_turned_on:

            if self.layout.system_on:
                print("SENDING BUTTON MESSAGE ON!")
                self.command_center.system_on = True
                self.system_turned_on = True
        else:
            if not self.layout.system_on:
                self.command_center.system_on = False
                self.system_turned_on = False


    def update_inputs(self, dt):
        self.layout.diluate_in_display = self.diluate_in_display
        self.layout.diluate_out_display = self.diluate_out_display
        self.layout.output_flow_display = self.output_flow_display


    def setServer(self, command_center, update_list):
        self.command_center = command_center
        self.update_list = update_list

    def build(self):
        self.layout = GUI_GridLayout()
        Clock.schedule_interval(self.update_buttons, 1.0)
        Clock.schedule_interval(self.update_inputs, 1.0)
        return self.layout

    def on_stop(self):
        print("APP CLOSED. SHUTTING DOWN…")
        self.command_center.stop_server()
        self.update_list.stop_server()


if __name__ == '__main__':
    apason_GUIApp().run()
