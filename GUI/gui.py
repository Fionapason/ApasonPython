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
    voltage_label_1 = StringProperty("Voltage 1?")
    voltage_label_2 = StringProperty("Voltage 2?")

    pressure_label_1 = StringProperty("Pressure 1:")
    pressure_label_2 = StringProperty("Pressure 2:")
    pressure_label_3 = StringProperty("Pressure 3:")

    pressure_display_1 = StringProperty()
    pressure_display_2 = StringProperty()
    pressure_display_3 = StringProperty()

    massflow_label_1 = StringProperty('Massflow 1:')
    massflow_label_2 = StringProperty('Massflow 2:')
    massflow_label_3 = StringProperty('Massflow 3:')

    massflow_display_1 = StringProperty()
    massflow_display_2 = StringProperty()
    massflow_display_3 = StringProperty()


    voltage_input_1 = TextInput()
    voltage_input_2 = TextInput()

    submit_button_label_1 = StringProperty("Submit 1")
    submit_button_label_2 = StringProperty("Submit 2")

    voltage_output_1 = NumericProperty(0)
    voltage_output_2 = NumericProperty(0)

    def press_1(self):
        voltage_1 = self.voltage_input_1.text
        self.voltage_output_1 = float(voltage_1)

    def press_2(self):
        voltage_2 = self.voltage_input_2.text
        self.voltage_output_2 = float(voltage_2)

    def build(self):
        # self.add_widget(Label(text=self.voltage_label_1))
        # self.add_widget(self.voltage_input_1)
        #
        # self.add_widget(Label(text=self.voltage_label_2))
        # self.add_widget(self.voltage_input_2)

        # self.submit_button_1 = Button(text=self.submit_button_label_1)
        # self.submit_button_1.bind(on_press=self.press_1)
        # self.add_widget(self.submit_button_1)

        # self.submit_button_2 = Button(text=self.submit_button_label_2)
        # self.submit_button_2.bind(on_press=self.press_2)
        # self.add_widget(self.submit_button_2)

        self.add_widget(Label(text=self.pressure_label_1))
        self.add_widget(Label(text=self.pressure_display_1))

        self.add_widget(Label(text=self.pressure_label_2))
        self.add_widget(Label(text=self.pressure_display_2))

        self.add_widget(Label(text=self.pressure_label_3))
        self.add_widget(Label(text=self.pressure_display_3))

        self.add_widget(Label(text=self.massflow_label_1))
        self.add_widget(Label(text=self.massflow_display_1))

        self.add_widget(Label(text=self.massflow_label_2))
        self.add_widget(Label(text=self.massflow_display_2))

        self.add_widget(Label(text=self.massflow_label_3))
        self.add_widget(Label(text=self.massflow_display_3))


class apason_GUIApp(App):
    command_center = None

    voltage_output_1 : float = 0
    voltage_output_2 : float = 0

    pressure_display_1 = StringProperty()
    pressure_display_2 = StringProperty()
    pressure_display_3 = StringProperty()

    massflow_display_1 = StringProperty()
    massflow_display_2 = StringProperty()
    massflow_display_3 = StringProperty()

    def update_outputs(self, dt):
        self.voltage_output_1 = self.layout.voltage_output_1
        self.voltage_output_2= self.layout.voltage_output_2

    def update_inputs(self, dt):
        self.layout.pressure_display_1 = self.pressure_display_1
        self.layout.pressure_display_2 = self.pressure_display_2
        self.layout.pressure_display_3 = self.pressure_display_3

        self.layout.massflow_display_1 = self.massflow_display_1
        self.layout.massflow_display_2 = self.massflow_display_2
        self.layout.massflow_display_3 = self.massflow_display_3

    def setServer(self, cc_server, sl_server):
        self.command_center = cc_server
        self.sensor_list = sl_server

    def build(self):
        self.layout = GUI_GridLayout()
        Clock.schedule_interval(self.update_outputs, 1.0)
        Clock.schedule_interval(self.update_inputs, 1.0)
        return self.layout

    def on_stop(self):
        self.command_center.stop_server()
        self.sensor_list.stop_server()


if __name__ == '__main__':
    apason_GUIApp().run()
