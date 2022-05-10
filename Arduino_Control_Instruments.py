#TODO TEST ALL OF THESE

import configurations_1 as conf_1
import configurations_2 as conf_2

"""
These classes define all the Arduino control instruments
They take their parameters from the configurations file
They are then all initialized in the Arduino_Control_Instruments class

Each instance of a type of control instrument has a unique ID, taken from the configurations file,
such that its corresponding instrument can be easily identified from the Command Center.

Also, each class instance has the id of the arduino it's plugged into as a class member,
also taken from the configurations file.

The digitally set classes (CV3, OCV, and Polarity) simply have the necessary commands as class members.

The classes, which can set analog voltages (Pump [and PCV]) have the function find_Voltage(wanted_value),
which returns the int from 0-4095 that needs to be set using sendV to attain the wanted_value.
These classes also have their respective DAC output as a member, also set in the configurations file.

THE ARDUINO_CONTROL_INSTRUMENTS OBJECTS ARE NOT *SUPPOSED* TO INTERACT DIRECTLY WITH THE ARDUINO
THE ARDUINOCOMMUNICATION CLASS IS RESPONSIBLE FOR THIS,
AND SIMPLY USES CLASS MEMBERS FROM HERE TO GET THE NECESSARY INFO
"""

# Parameters: max_RPM, DAC_output, arduino_id, id
# Function: find_Voltage(rpm)

class Pump:
    '''**Parameters:** max_RPM, DAC_output, arduino_id, id \n
    **Function:** find_Voltage(rpm)'''

#    command_on : str

    max_RPM : float

    DAC_output : str

    arduino_id: int

    id : int


    def __init__(self, max, DAC, arduino_id, id):
        self.max_RPM = max
        self.DAC_output = DAC
        self.arduino_id = arduino_id
        self.id = id
        # self.command_on = command_on

    #returns the int from 0-4095 which corresponds to the wanted rpm
    def find_Voltage(self, rpm):
        return int((rpm / self.max_RPM) * 4095)

# # Parameters: DAC_output, arduino_id, id
# # Function: find_Voltage(percent)
#
# class PCV:
#
#     '''**Parameters:** DAC_output, arduino_id, id \n
#     **Function:** find_Voltage(percent)'''
#
#     DAC_output: str
#
#     arduino_id: int
#
#     id : int
#
#
#     def __init__(self, DAC, arduino_id, id):
#         self.DAC_output = DAC
#         self.arduino_id = arduino_id
#         self.id = id
#
#     def find_Voltage(self, percent):
#         return int((percent / 100) * 4095)

# Parameters: command_open, command_close, arduino_id, id

class OCV_normallyOpen:
    '''
    **Parameters:** command_open, command_close, arduino_id, id
    '''

    command_low : str

    command_high : str

    arduino_id : int

    id : int

    def __init__(self, command_open, command_close, arduino_id, id):
        self.command_low = command_open
        self.command_high = command_close
        self.arduino_id = arduino_id
        self.id = id

# Parameters: command_open, command_close, arduino_id, id

class OCV_normallyClosed:
    '''
    **Parameters:** command_open, command_close, arduino_id, id
    '''

    command_high: str

    command_low: str

    arduino_id: int

    id: int

    def __init__(self, command_open, command_close, arduino_id, id):
        self.command_high = command_open
        self.command_low = command_close
        self.arduino_id = arduino_id
        self.id = id

# Parameters: command_low, command_high, arduino_id, id

class CV3:
    '''
    **Parameters:** command_low, command_high, arduino_id, id
    '''

    command_high: str

    command_low: str

    arduino_id: int

    id: int

    def __init__(self, command_high, command_low, arduino_id, id):
        self.command_high = command_high
        self.command_low = command_low
        self.arduino_id = arduino_id
        self.id = id

# Parameters: command_pos, command_neg, arduino_id, id

class Polarity:
    '''
    **Parameters:** command_pos, command_neg, arduino_id, id
    '''

    command_low = '('

    command_high = ')'

    command_off = '*'

    arduino_id : int

    id: int

    def __init__(self, arduino_id, id):
        self.arduino_id = arduino_id
        self.command_low =  bytes(self.command_low, 'utf-8')
        self.command_high = bytes(self.command_high, 'utf-8')
        self.command_off = bytes(self.command_off, 'utf-8')
        self.id = id

# The class contains all the control instruments that are currently in use
# It keeps each instrument in a list called [type]_instruments
# Except polarity, which is unique
# Using the configurations file and its internally saved command lists, it builds the class instances iteratively

class Arduino_Control_Instruments:
    '''**Parameters**: *lists:*  pump_instruments, pcv_instruments, ocv_normally_open_instruments, ocv_normally_closed_instruments, cv3_instruments \n
    ocv_normally_open_open_commands, ocv_normally_open_close_commands, ocv_normally_closed_open_commands, ocv_normally_closed_close_commands, cv3_high_commands, cv3_high_commands'''

    # The control instruments are kept in an ordered list, which in turn is a class member

    pump_instruments = []
    # pcv_instruments = []
    ocv_normally_open_instruments = []
    ocv_normally_closed_instruments = []
    cv3_instruments = []

    # CAREFUL! The index within this list is NOT necessarily equivalent to the id, taken from the configurations
    # However, if configurations are "filled" from the bottom up, they should be identical

    # The commands to be sent to the arduino,
    # all single characters to make serial communication as simple as possible
    ocv_normally_closed_open_commands = ['R', 'S', 'T']
    ocv_normally_closed_close_commands = ['V', 'W', 'X']

    ocv_normally_open_open_commands = ['U']
    ocv_normally_open_close_commands = ['Y']

    cv3_high_commands = ['F', 'G', 'H', 'I', 'J', 'K']
    cv3_low_commands = ['L', 'M', 'N', 'O', 'P', 'Q']

    # These are hard-coded and should not be changed without also changing the arduino code!

    def __init__(self):

        # Iterate through every instrument of a specific type in the configurations files,
        for instrument in conf_1.control_instrument_configurations_1["pump"]:
            # Check if the current instrument is marked as "in use"
            if instrument["in_use"]:
                # Use the configurations file to build the new instrument object, using the parameters from the configurations file
                new_pump = Pump(max=instrument["max_RPM"],
                                DAC=instrument["DAC_output"],
                                arduino_id=instrument["arduino_id"],
                                id=instrument["id"])
                # Append the instrument object to its respective list
                self.pump_instruments.append(new_pump)
        # Repeat with all classes
        # for instrument in conf_1.control_instrument_configurations_1["pcv"]:
        #     if instrument["in_use"]:
        #         new_pcv = PCV(DAC=instrument["DAC_output"],
        #                       arduino_id=instrument["arduino_id"],
        #                       id=instrument["id"])
        #         self.pcv_instruments.append(new_pcv)

        for instrument in conf_1.control_instrument_configurations_1["cv3"]:
            if instrument["in_use"]:

                index = instrument["id"]

                current_command_high = bytes(self.cv3_high_commands[index], 'utf-8')
                current_command_low = bytes(self.cv3_low_commands[index], 'utf-8')

                new_cv3 = CV3(command_high=current_command_high,
                              command_low=current_command_low,
                              arduino_id=instrument["arduino_id"],
                              id=instrument["id"])
                self.cv3_instruments.append(new_cv3)

        for instrument in conf_1.control_instrument_configurations_1["ocv_normally_open"]:
            if instrument["in_use"]:

                index = instrument["id"]

                current_open_command = bytes(self.ocv_normally_open_open_commands[index], 'utf-8')
                current_close_command = bytes(self.ocv_normally_open_close_commands[index], 'utf-8')

                new_ocv_no = OCV_normallyOpen(command_open=current_open_command,
                                              command_close=current_close_command,
                                              arduino_id=instrument["arduino_id"],
                                              id=index)
                self.ocv_normally_open_instruments.append(new_ocv_no)

        for instrument in conf_1.control_instrument_configurations_1["ocv_normally_closed"]:
            if instrument["in_use"]:

                index = instrument["id"]

                current_open_command = bytes(self.ocv_normally_closed_open_commands[index], 'utf-8')
                current_close_command = bytes(self.ocv_normally_closed_close_commands[index], 'utf-8')

                new_ocv_nc = OCV_normallyClosed(command_open=current_open_command,
                                              command_close=current_close_command,
                                              arduino_id=instrument["arduino_id"],
                                              id=index)

                self.ocv_normally_closed_instruments.append(new_ocv_nc)

        for instrument in conf_1.control_instrument_configurations_1["polarity"]:
            if instrument["in_use"]:
                # Since there is only one ED module, polarity is simply a class member and is not appended to a list
                self.polarity = Polarity(arduino_id=instrument["arduino_id"],
                                         id=instrument["id"])

        # Repeat for the instruments on the second arduino

        for instrument in conf_2.control_instrument_configurations_2["pump"]:
            # Check if the current instrument is marked as "in use"
            if instrument["in_use"]:
                # Use the configurations file to build the new instrument object, using the parameters from the configurations file
                new_pump = Pump(max=instrument["max_RPM"],
                                DAC=instrument["DAC_output"],
                                arduino_id=instrument["arduino_id"],
                                id=instrument["id"])
                # Append the instrument object to its respective list
                self.pump_instruments.append(new_pump)

        # for instrument in conf_2.control_instrument_configurations_2["pcv"]:
        #     if instrument["in_use"]:
        #         new_pcv = PCV(DAC=instrument["DAC_output"],
        #                       arduino_id=instrument["arduino_id"],
        #                       id=instrument["id"])
        #         self.pcv_instruments.append(new_pcv)

        for instrument in conf_2.control_instrument_configurations_2["cv3"]:
            if instrument["in_use"]:

                # Start over in the command list vector
                index = len(self.cv3_high_commands) - instrument["id"]

                current_command_high = bytes(self.cv3_high_commands[index], 'utf-8')
                current_command_low = bytes(self.cv3_low_commands[index], 'utf-8')

                new_cv3 = CV3(command_high=current_command_high,
                              command_low=current_command_low,
                              arduino_id=instrument["arduino_id"],
                              id=instrument["id"])
                self.cv3_instruments.append(new_cv3)

        for instrument in conf_2.control_instrument_configurations_2["ocv_normally_open"]:
            if instrument["in_use"]:


                index = len(self.ocv_normally_open_instruments) - instrument["id"]

                current_open_command = bytes(self.ocv_normally_open_open_commands[index], 'utf-8')
                current_close_command = bytes(self.ocv_normally_open_close_commands[index], 'utf-8')

                new_ocv_no = OCV_normallyOpen(command_open=current_open_command,
                                              command_close=current_close_command,
                                              arduino_id=instrument["arduino_id"],
                                              id=index)
                self.ocv_normally_open_instruments.append(new_ocv_no)

        for instrument in conf_2.control_instrument_configurations_2["ocv_normally_closed"]:
            if instrument["in_use"]:

                index = len(self.ocv_normally_closed_open_commands) - instrument["id"]

                current_open_command = bytes(self.ocv_normally_closed_open_commands[index], 'utf-8')
                current_close_command = bytes(self.ocv_normally_closed_close_commands[index], 'utf-8')

                new_ocv_nc = OCV_normallyClosed(command_open=current_open_command,
                                              command_close=current_close_command,
                                              arduino_id=instrument["arduino_id"],
                                              id=index)

                self.ocv_normally_closed_instruments.append(new_ocv_nc)

        for instrument in conf_2.control_instrument_configurations_2["polarity"]:
            if instrument["in_use"]:
                # Since there is only one ED module, polarity is simply a class member and is not appended to a list
                self.polarity = Polarity(arduino_id=instrument["arduino_id"],
                                         id=instrument["id"])

if __name__ == '__main__':
    attempt = Arduino_Control_Instruments()

    for pump in attempt.pump_instruments:
        print(pump.id)