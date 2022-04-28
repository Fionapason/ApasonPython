import configurations as conf
import ArduinoCommunication

class Pump:

    command_on : str

    max_RPM : float

    DAC_output : str

    arduino_id: int

    id : int


    def __init__(self, max, command_on, DAC, arduino_id, id):
        self.max_RPM = max
        self.command_on = command_on
        self.DAC_output = DAC
        self.arduino_id = arduino_id
        self.id = id

    def find_Voltage(self, rpm):
        return int((rpm / self.max_RPM) * 4095)

class PCV:

    DAC_output: str

    arduino_id: int

    id : int


    def __init__(self, command, DAC, arduino_id, id):
        self.command = command
        self.DAC_output = DAC
        self.arduino_id = arduino_id
        self.id = id

    def find_Voltage(self, percent):
        return int((percent / 100) * 4095)

class OCV_normallyOpen:

    command_open : str

    command_close : str

    arduino_id : int

    id : int

    def __init__(self, command_open, command_close, arduino_id, id):
        self.command_open = command_open
        self.command_close = command_close
        self.arduino_id = arduino_id
        self.id = id

class OCV_normallyClosed:

    command_open: str

    command_close: str

    arduino_id: int

    id: int

    def __init__(self, command_open, command_close, arduino_id, id):
        self.command_open = command_open
        self.command_close = command_close
        self.arduino_id = arduino_id
        self.id = id

class CV3:

    command_high: str

    command_low: str

    arduino_id: int

    id: int

    def __init__(self, command_open, command_close, arduino_id, id):
        self.command_high = command_open
        self.command_low = command_close
        self.arduino_id = arduino_id
        self.id = id

class Polarity:

    command_pos = '('

    command_neg = ')'

    arduino_id : int

    id: int

    def __init__(self, arduino_id, id):
        self.arduino_id = arduino_id
        self.id = id

class Arduino_Control_Instruments:

    pump_instruments = []

    pcv_instruments = []

    polarity_instrument = []


    OCV_normallyOpen_Open_commands = ['R', 'S', 'T']
    OCV_normallyOpen_Close_commands = ['V', 'W', 'X']
    OCV_normallyOpen_instruments = []

    OCV_normallyClosed_Open_commands = ['U']
    OCV_normallyClosed_Close_commands = ['Y']
    OCV_normallyClosed_instruments = []

    CV3_high_commands = ['F', 'G', 'H', 'I', 'J', 'K']
    CV3_low_commands = ['L', 'M', 'N', 'O', 'P', 'Q']
    CV3_instruments = []

    def __init__(self):

        for instrument in conf.control_instrument_configurations["CV3"]:
            pass
