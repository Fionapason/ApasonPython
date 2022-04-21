from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.button import Button

from server import GetVoltage


class GUI_GridLayout(GridLayout):
    voltage_label_1 = StringProperty("Voltage 1?")
    voltage_label_2 = StringProperty("Voltage 2?")

    voltage_input_1 = TextInput()
    voltage_input_2 = TextInput()

    submit_button_label_1 = StringProperty("Submit 1")
    submit_button_label_2 = StringProperty("Submit 2")

    voltage_output_1 = NumericProperty(0)
    voltage_output_2 = NumericProperty(0)

    server: GetVoltage

    def press_1(self):
        voltage_1 = self.voltage_input_1.text
        self.voltage_output_1 = float(voltage_1)
        self.server.voltage_1 = float(voltage_1)

    def press_2(self):
        voltage_2 = self.voltage_input_2.text
        self.voltage_output_2 = float(voltage_2)
        self.server.voltage_2 = float(voltage_2)

    def build(self):
        self.add_widget(Label(text=self.voltage_label_1))
        self.add_widget(self.voltage_input_1)

        self.add_widget(Label(text=self.voltage_label_2))
        self.add_widget(self.voltage_input_2)

        self.submit_button_1 = Button(text=self.submit_button_label_1)
        self.submit_button_1.bind(on_press=self.press_1)
        self.add_widget(self.submit_button_1)

        self.submit_button_2 = Button(text=self.submit_button_label_2)
        self.submit_button_2.bind(on_press=self.press_2)
        self.add_widget(self.submit_button_2)


class apason_GUIApp(App):
    server = None

    def setServer(self, server):
        self.server = server

    def build(self):
        layout = GUI_GridLayout()
        layout.server = self.server
        return layout

    def on_stop(self):
        self.server.stop()


# class GUI_Window(Widget):
#     def build(self):
#         return GUI_GridLayout(voltage='Voltage ?')


if __name__ == '__main__':
    apason_GUIApp().run()
