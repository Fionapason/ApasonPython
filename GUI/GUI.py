from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.button import Button

class GUI_GridLayout(GridLayout):

    voltage_label = StringProperty("Voltage ?")

    def build(self):
        self.voltage_label = "Voltage ?"
        self.add_widget(Label(text=self.voltage_label))
        self.voltage_input = TextInput(multiline=False)
        self.add_widget(self.voltage_input)

class apason_GUIApp(App):
    def build(self):
        return GUI_GridLayout(voltage_label="Voltage ?")

# class GUI_Window(Widget):
#     def build(self):
#         return GUI_GridLayout(voltage='Voltage ?')




if __name__ == '__main__':
    apason_GUIApp().run()