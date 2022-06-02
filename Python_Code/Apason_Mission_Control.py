import Main_Threads.GUI.gui as gui
from Arduino_Communication import Arduino_Sensors, Arduino_Control_Instruments as ard_control_ins, \
    Arduino_Utilities as ard_com
from Sensor_Instrument_Tracking import Sensor_Update_List as ulist
from Main_Threads.Command_Center_Thread import Command_Center
from Main_Threads.Update_List_Thread import Update_List

if __name__ == '__main__':

    # Set up the serial communication with both arduinos
    arduinos = ard_com.Arduino_Utilities()

    # Initialize the Arduino Sensor/Instruments
    sensors = Arduino_Sensors.Arduino_Sensors()
    control_instruments = ard_control_ins.Arduino_Control_Instruments()

    # Initialize the update list
    update_list = ulist.Sensor_Update_List()

    # Initialize the Interface but don't start it yet
    interface: gui.apason_GUIApp = gui.apason_GUIApp()

    # Initialize and start the Update List and Command Center threads
    update = Update_List(interface=interface,
                         list=update_list,
                         arduino=arduinos,
                         arduino_sensors=sensors)
    command_center = Command_Center(arduinos=arduinos,
                                    ard_control=control_instruments,
                                    update_list=update_list,
                                    interface=interface)

    # Make sure the GUI has access to the Update List and the Command Center
    interface.set_server(command_center, update)

    # Finally start the GUI thread.
    interface.run()
