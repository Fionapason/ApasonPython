
import configurations_1 as conf_1
import configurations_2 as conf_2

# global variable for all voltage measurements
analogReference = 5.0
# global variable for all current source sensors
minVolt_current = 1.0

"""
These classes define all the Arduino sensors
They take their parameters from the configurations file
They are then all initialized in the Arduino_Sensors class

Each instance of a type of control instrument has a unique ID, taken from the configurations file,
such that its corresponding instrument can be easily identified from the Update List.

Also, each class instance has the id of the arduino it's plugged into as a class member,
also taken from the configurations file.

Class instances also have certain sensor-dependent mathematical parameters as members, again from the conf files.

Each class instance has the needed arduino command as a member, to be able to easily retrieve a measurment.
Additionally, each class, with the exception of Switch, has the function currentValue,
which takes a raw measurement (int from 0 to 1023) and, based on class class members and the global variables,
returns the true measurement of the sensor.

THE ARDUINO_SENSORS OBJECTS ARE NOT *SUPPOSED* TO INTERACT DIRECTLY WITH THE ARDUINO
THE ARDUINOCOMMUNICATION CLASS IS RESPONSIBLE FOR THIS,
AND SIMPLY USES CLASS MEMBERS FROM HERE TO GET THE NECESSARY INFO
"""

# Parameters: command, max_pressure, arduino_id, id
# Function: currentValue(raw_measurement)

class Pressure:
    '''**Parameters:** command, max_pressure, arduino_id, id
    **Functions:** currentValue(raw_measurement)'''
    command : str

    max_pressure : float

    arduino_id : int

    id : int

    def __init__(self, max, command, id, arduino_id):
        self.max_pressure = max
        self.command = command
        self.id = id
        self.arduino_id = arduino_id

    def currentValue(self, raw_measurement):
        return float(raw_measurement) * analogReference * self.max_pressure / (1023.0 * 5.0)

# Parameters: command, graph_constant, max_massflow, min_massflow = 0, arduino_id, id
# Function: currentValue(raw_measurement)

class Massflow:
    '''**Parameters:** command, max_pressure, arduino_id, id
    **Functions:** currentValue(raw_measurement)'''

    command : str

    graph_constant : float

    max_massflow : float

    min_massflow = 0

    arduino_id: int

    id : int

    def __init__(self, max, command, id, arduino_id):
        self.max_massflow = max
        self.command = command
        self.id = id
        self.arduino_id = arduino_id
        self.graph_constant = self.max_massflow-((self.max_massflow-self.min_massflow)/(analogReference-minVolt_current))*analogReference

    def currentValue(self, raw_measurement):
        return float(raw_measurement) * (analogReference / 1023.0) * (self.max_massflow-self.min_massflow)/(analogReference-minVolt_current) + self.graph_constant

# Parameters: command, graph_constant, max_cond, min_cond, arduino_id, id
# Function: currentValue(raw_measurement)

class Conductivity:
    '''**Parameters:** command, graph_constant, max_cond, min_cond, arduino_id, id
    **Functions:** currentValue(raw_measurement)'''

    command : str

    graph_constant : float

    max_cond : float

    min_cond : float

    arduino_id : int

    id : int

    def __init__(self, max, min, command, arduino_id, id):
        self.max_cond = max
        self.min_cond = min
        self.command = command
        self.id = id
        self.arduino_id = arduino_id
        self.graph_constant = self.max_cond - ((self.max_cond - self.min_cond) / (analogReference - minVolt_current)) * analogReference

    def currentValue(self, raw_measurement):
        return float(raw_measurement) * (analogReference / 1023.0) * (self.max_cond - self.min_cond) / (
                    analogReference - minVolt_current) + self.graph_constant

# Parameters: command, graph_constant, max_temp, min_temp, arduino_id, id
# Function: currentValue(raw_measurement)

# class Temperature:
#     '''**Parameters:** command, graph_constant, max_temp, min_temp, arduino_id, id
#     **Functions:** currentValue(raw_measurement)'''
#
#     command : str
#
#     graph_constant : float
#
#     max_temp : float
#
#     min_temp : float
#
#     arduino_id : int
#
#     id : int
#
#     def __init__(self, max, command, arduino_id, id):
#         self.max_temp = max
#         self.min_temp = 0
#         self.command = command
#         self.id = id
#         self.arduino_id = arduino_id
#         self.graph_constant = self.max_temp - ((self.max_temp - self.min_temp) / (analogReference - minVolt_current)) * analogReference
#
#
#     def currentValue(self, raw_measurement):
#         return float(raw_measurement) * (analogReference / 1023.0) * (self.max_temp - self.min_temp) / (analogReference - minVolt_current) + self.graph_constant

# Parameters: command, arduino_id, id

class Switch:
    '''*Parameters:* command, arduino_id, id'''
    command: str

    arduino_id : int

    id : int

    def __init__(self, command, arduino_id, id):
        self.command = command
        self.id = id
        self.arduino_id = arduino_id



class Arduino_Sensors:
    '''**Parameters:** *lists:* pressure_sensors, massflow_sensors, conductivity_sensors, temperature_sensors, levelswitch_sensors \n
    pressure_commands, massflow_commands, conductivity_commands, temperature_commands, levelswitch_commands'''

    # The sensors are kept in an ordered list, which in turn is a class member

    pressure_sensors = []
    massflow_sensors = []
    conductivity_sensors = []
    # temperature_sensors = []
    levelswitch_sensors = []

    # CAREFUL! The index within this list is NOT necessarily equivalent to the id, taken from the configurations
    # However, if configurations are "filled" from the bottom up, they should be identical

    # The commands to be sent to the arduino,
    # all single characters to make serial communication as simple as possible

    pressure_commands = ['a', 'b', 'c', 'd', 'e']
    massflow_commands = ['f', 'g', 'h', 'i']
    conductivity_commands = ['j', 'k', 'l']
    # temperature_commands = ['m', 'n', 'o'] # p, if Mouser
    levelswitch_commands = ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E']

    # These are hard-coded and should not be changed without also changing the arduino code!

    def __init__(self):

        # Iterate through every sensor of a specific type in the configurations file
        for sensor in conf_1.sensor_configurations_1["pressure"]:
            # Check if sensor in use
            if sensor["in_use"]:
                #Get index for command
                index = sensor["id"]

                current_command = bytes(self.pressure_commands[index], 'utf-8')
                # Build sensor
                new_pressure_sensor = Pressure(max=sensor["max_pressure"],
                                               command=current_command,
                                               id=sensor["id"],
                                               arduino_id=sensor["arduino_id"])
                # Add sensor to list
                self.pressure_sensors.append(new_pressure_sensor)

        # The same for every sensor
        for sensor in conf_1.sensor_configurations_1["massflow"]:

            index = sensor["id"]

            if sensor["in_use"]:
                current_command = bytes(self.massflow_commands[index], 'utf-8')
                new_massflow_sensor = Massflow(max=sensor["max_flow"],
                                               command=current_command,
                                               id=sensor["id"],
                                               arduino_id=sensor["arduino_id"])
                self.massflow_sensors.append(new_massflow_sensor)

        for sensor in conf_1.sensor_configurations_1["conductivity"]:

            index = sensor["id"]

            if sensor["in_use"]:
                current_command = bytes(self.conductivity_commands[index], 'utf-8')
                new_conductivity_sensor = Conductivity(max=sensor["max_Cond"],
                                                       min=sensor["min_Cond"],
                                                       command=current_command,
                                                       id=sensor["id"],
                                                       arduino_id=sensor["arduino_id"])
                self.conductivity_sensors.append(new_conductivity_sensor)

        # for sensor in conf_1.sensor_configurations_1["temperature"]:
        #
        #     index = sensor["id"]
        #
        #     if sensor["in_use"]:
        #         current_command = bytes(self.temperature_commands[index], 'utf-8')
        #         new_temperature_sensor = Temperature(max=sensor["max_Temp"],
        #                                               command=current_command, id=sensor["id"],
        #                                               arduino_id=sensor["arduino_id"])
        #         self.temperature_sensors.append(new_temperature_sensor)

        for sensor in conf_1.sensor_configurations_1["level"]:

            index = sensor["id"]

            if sensor["in_use"]:
                current_command = bytes(self.levelswitch_commands[index], 'utf-8')
                new_level_switch = Switch(command=current_command,
                                          id=sensor["id"],
                                          arduino_id=sensor["arduino_id"])
                self.levelswitch_sensors.append(new_level_switch)


        # The same for sensors on arduino 2
        for sensor in conf_2.sensor_configurations_2["pressure"]:

            if sensor["in_use"]:

                # Adjust command index
                index = sensor["id"] - len(self.pressure_commands)

                current_command = bytes(self.pressure_commands[index], 'utf-8')
                new_pressure_sensor = Pressure(max=sensor["max_pressure"],
                                               command=current_command,
                                               id=index,
                                               arduino_id=sensor["arduino_id"])
                self.pressure_sensors.append(new_pressure_sensor)

        for sensor in conf_2.sensor_configurations_2["massflow"]:

            index = sensor["id"] - len(self.massflow_commands)

            if sensor["in_use"]:
                current_command = bytes(self.massflow_commands[index], 'utf-8')
                new_massflow_sensor = Massflow(max=sensor["max_flow"],
                                               command=current_command,
                                               id=sensor["id"],
                                               arduino_id=sensor["arduino_id"])
                self.massflow_sensors.append(new_massflow_sensor)

        for sensor in conf_2.sensor_configurations_2["conductivity"]:

            index = sensor["id"] - len(self.conductivity_commands)

            if sensor["in_use"]:
                index_ = self.conductivity_commands[index]
                current_command = bytes(index_, 'utf-8')
                new_conductivity_sensor = Conductivity(max=sensor["max_Cond"],
                                                       min=sensor["min_Cond"],
                                                       command=current_command,
                                                       id=sensor["id"],
                                                       arduino_id=sensor["arduino_id"])
                self.conductivity_sensors.append(new_conductivity_sensor)


        # for sensor in conf_2.sensor_configurations_2["temperature"]:
        #
        #     index = len(self.temperature_commands) - sensor["id"]
        #
        #     if sensor["in_use"]:
        #         current_command = bytes(self.temperature_commands[index], 'utf-8')
        #         new_temperature_sensor = Temperature(max=sensor["max_Temp"],
        #                                               command=current_command, id=sensor["id"],
        #                                               arduino_id=sensor["arduino_id"])
        #         self.temperature_sensors.append(new_temperature_sensor)

        for sensor in conf_2.sensor_configurations_2["level"]:

            index = sensor["id"] - len(self.levelswitch_commands)

            if sensor["in_use"]:
                current_command = bytes(self.levelswitch_commands[index], 'utf-8')
                new_level_switch = Switch(command=current_command,
                                          id=sensor["id"],
                                          arduino_id=sensor["arduino_id"])
                self.levelswitch_sensors.append(new_level_switch)



if __name__ == '__main__':

    try_list = Arduino_Sensors()

    for sensor in try_list.pressure_sensors:
        print(sensor.id)

    for sensor in try_list.massflow_sensors:
        print(sensor.id)

    for sensor in try_list.conductivity_sensors:
        print(sensor.id)

    # for sensor in try_list.temperature_sensors:
    #     print(sensor.id)

    for sensor in try_list.levelswitch_sensors:
        print(sensor.id)
