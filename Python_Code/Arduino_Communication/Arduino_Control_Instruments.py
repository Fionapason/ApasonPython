from Configurations import Configurations_Arduino_ED as conf_ed, Configurations_Arduino_UF as conf_uf

"""
These classes define all the Arduino control instruments
They take their parameters from the configurations files
They are then all initialized in the Arduino_Control_Instruments class

Each instance of a type of control instrument has a unique ID, taken from the configurations file.

Also, each class instance has the ID of the arduino it's plugged into as a class member,
also taken from the configurations file.

The digitally set classes (CV3, OCV, and Polarity) simply have the necessary commands as class members.

Pump objects can additionally set analog voltages, using the function find_voltage(wanted_value),
which returns the int from 0-4095 that needs to be set to attain the wanted_value.
This also has its respective DAC output as a member, also set in the configurations file.

THE ARDUINO_CONTROL_INSTRUMENTS OBJECTS ARE NOT *SUPPOSED* TO INTERACT DIRECTLY WITH THE ARDUINO!

THE ARDUINO_UTILITIES CLASS IS RESPONSIBLE FOR THIS,
AND SIMPLY USES CLASS MEMBERS FROM HERE TO GET THE NECESSARY INFO
"""


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

    # returns the int from 0-4095 which corresponds to the wanted rpm
    def find_voltage(self, rpm):
        return int((rpm / self.max_RPM) * 4095)



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



class Polarity:
    '''
    **Parameters:** command_pos, command_neg, command_off arduino_id, id
    '''

    # since Polarity is a unique instrument within Apasōn, its commands are unambiguous.

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
# Using the configurations files and its internally saved command lists, it builds the class instances iteratively

class Arduino_Control_Instruments:
    '''**Parameters**: *lists:*  pump_instruments, ocv_normally_open_instruments, ocv_normally_closed_instruments, cv3_instruments \n
    ocv_normally_open_open_commands, ocv_normally_open_close_commands, ocv_normally_closed_open_commands, ocv_normally_closed_close_commands, cv3_high_commands, cv3_high_commands'''

    # The control instruments are kept in an ordered list, which in turn is a class member

    pump_instruments = []
    ocv_normally_open_instruments = []
    ocv_normally_closed_instruments = []
    cv3_instruments = []

    # CAREFUL! The index within this list is NOT necessarily equivalent to the id, taken from the configurations
    # However, if configurations are "filled" from the bottom up, they should be identical

    # The commands to be sent to the Arduino,
    # all single characters to make serial communication as simple as possible
    ocv_normally_closed_open_commands = ['R', 'S', 'T']
    ocv_normally_closed_close_commands = ['V', 'W', 'X']

    ocv_normally_open_open_commands = ['U']
    ocv_normally_open_close_commands = ['Y']

    cv3_high_commands = ['F', 'G', 'H', 'I', 'J', 'K']
    cv3_low_commands = ['L', 'M', 'N', 'O', 'P', 'Q']

    # These are hard-coded and should *not* be changed without also changing the arduino code!

    def __init__(self):

        # We begin on the UF Arduino

        # Iterate through every instrument of a specific type in the configurations files,
        for instrument in conf_uf.control_instrument_configurations_uf["pump"]:
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

        for instrument in conf_uf.control_instrument_configurations_uf["cv3"]:
            if instrument["in_use"]:

                index = instrument["id"]

                current_command_high = bytes(self.cv3_high_commands[index], 'utf-8')
                current_command_low = bytes(self.cv3_low_commands[index], 'utf-8')

                new_cv3 = CV3(command_high=current_command_high,
                              command_low=current_command_low,
                              arduino_id=instrument["arduino_id"],
                              id=instrument["id"])
                self.cv3_instruments.append(new_cv3)

        for instrument in conf_uf.control_instrument_configurations_uf["ocv_normally_open"]:
            if instrument["in_use"]:

                index = instrument["id"]

                current_open_command = bytes(self.ocv_normally_open_open_commands[index], 'utf-8')
                current_close_command = bytes(self.ocv_normally_open_close_commands[index], 'utf-8')

                new_ocv_no = OCV_normallyOpen(command_open=current_open_command,
                                              command_close=current_close_command,
                                              arduino_id=instrument["arduino_id"],
                                              id=index)
                self.ocv_normally_open_instruments.append(new_ocv_no)

        for instrument in conf_uf.control_instrument_configurations_uf["ocv_normally_closed"]:
            if instrument["in_use"]:

                index = instrument["id"]

                current_open_command = bytes(self.ocv_normally_closed_open_commands[index], 'utf-8')
                current_close_command = bytes(self.ocv_normally_closed_close_commands[index], 'utf-8')

                new_ocv_nc = OCV_normallyClosed(command_open=current_open_command,
                                              command_close=current_close_command,
                                              arduino_id=instrument["arduino_id"],
                                              id=index)

                self.ocv_normally_closed_instruments.append(new_ocv_nc)

        # Repeat for the instruments on the ED Arduino

        for instrument in conf_ed.control_instrument_configurations_ed["pump"]:
            # Check if the current instrument is marked as "in use"
            if instrument["in_use"]:
                # Use the configurations file to build the new instrument object, using the parameters from the configurations file
                new_pump = Pump(max=instrument["max_RPM"],
                                DAC=instrument["DAC_output"],
                                arduino_id=instrument["arduino_id"],
                                id=instrument["id"])
                # Append the instrument object to its respective list
                self.pump_instruments.append(new_pump)


        for instrument in conf_ed.control_instrument_configurations_ed["cv3"]:
            if instrument["in_use"]:

                # Start over in the command list vector, as both Arduinos use the same code
                index = instrument["id"] - len(self.cv3_high_commands)
                current_command_high = bytes(self.cv3_high_commands[index], 'utf-8')
                current_command_low = bytes(self.cv3_low_commands[index], 'utf-8')

                new_cv3 = CV3(command_high=current_command_high,
                              command_low=current_command_low,
                              arduino_id=instrument["arduino_id"],
                              id=instrument["id"])
                self.cv3_instruments.append(new_cv3)

        for instrument in conf_ed.control_instrument_configurations_ed["ocv_normally_open"]:
            if instrument["in_use"]:


                index = instrument["id"] - len(self.cv3_high_commands)


                current_open_command = bytes(self.ocv_normally_open_open_commands[index], 'utf-8')
                current_close_command = bytes(self.ocv_normally_open_close_commands[index], 'utf-8')

                new_ocv_no = OCV_normallyOpen(command_open=current_open_command,
                                              command_close=current_close_command,
                                              arduino_id=instrument["arduino_id"],
                                              id=index)
                self.ocv_normally_open_instruments.append(new_ocv_no)

        for instrument in conf_ed.control_instrument_configurations_ed["ocv_normally_closed"]:
            if instrument["in_use"]:

                index = instrument["id"] - len(self.cv3_high_commands)

                current_open_command = bytes(self.ocv_normally_closed_open_commands[index], 'utf-8')
                current_close_command = bytes(self.ocv_normally_closed_close_commands[index], 'utf-8')

                new_ocv_nc = OCV_normallyClosed(command_open=current_open_command,
                                              command_close=current_close_command,
                                              arduino_id=instrument["arduino_id"],
                                              id=index)

                self.ocv_normally_closed_instruments.append(new_ocv_nc)

        for instrument in conf_ed.control_instrument_configurations_ed["polarity"]:
            if instrument["in_use"]:
                # Since there is only one ED module, polarity is simply a class member and is not appended to a list
                self.polarity = Polarity(arduino_id=instrument["arduino_id"],
                                         id=instrument["id"])

