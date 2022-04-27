import configurations as conf

analogReference = 5.0

minVolt_current = 1.0

#TODO add arduino index to clear up

class Pressure:

    command : str

    max_pressure : float

    id : int

    def __init__(self, max, command, id):
        self.max_pressure = max
        self.command = command
        self.id = id

    def currentValue(self, raw_measurement):
        return float(raw_measurement) * analogReference * self.max_pressure / (1023.0 * 5.0)

class Massflow:

    command : str

    graph_constant : float

    max_massflow : float

    min_massflow = 0

    id : int

    def __init__(self, max, command, id):
        self.max_massflow = max
        self.command = command
        self.id = id
        self.graph_constant = self.max_massflow-((self.max_massflow-self.min_massflow)/(analogReference-minVolt_current))*analogReference

    def currentValue(self, raw_measurement):
        return float(raw_measurement) * (analogReference / 1023.0) * (self.max_massflow-self.min_massflow)/(analogReference-minVolt_current) + self.graph_constant

#TODO
class Pressure_Gems:

    commands = ['a']

    max_pressure: float

    id : int

    def __init__(self, max, command, id):
        self.max_pressure = max
        self.command = command
        self.id = id

    def currentValue(self):
        pass

class Conducitivty:

    def __init__(self, max, command, id):
        pass
    def currentValue(self):
        pass

class Temperature:
    def __init__(self, max, command, id):
        pass

    def currentValue(self):
        pass

class Switch:
    def __init__(self, max, command, id):
        pass

    def currentValue(self):
        pass




class Arduino_Sensors:


    pressure_commands = ['b', 'c', 'd', 'e']
    pressure_sensors = []

    massflow_commands = ['f', 'g', 'h', 'i']
    massflow_sensors = []

    conductivity_commands = ['j', 'k', 'l']
    conductivity_sensors = []

    temperature_commands = ['m', 'n', 'o']
    temperature_sensors = []

    levelswitch_commands = ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E']
    levelswitch_sensors = []


    def __init__(self):

        index = 0


        for sensor in conf.sensor_configurations["pressure"]:

            if sensor["in_use"]:

                current_command = bytes(self.pressure_commands[index], 'utf-8')
                new_pressure_sensor = Pressure(sensor["max_pressure"], current_command, index)
                self.pressure_sensors.append(new_pressure_sensor)
                index += 1

        index = 0

        for sensor in conf.sensor_configurations["massflow"]:

            if sensor["in_use"]:
                current_command = bytes(self.massflow_commands[index], 'utf-8')
                new_massflow_sensor = Massflow(sensor["max_flow"], current_command, index)
                self.massflow_sensors.append(new_massflow_sensor)
                index += 1

        #TODO
        for sensor in conf.sensor_configurations["conductivity"]:
            pass

        for sensor in conf.sensor_configurations["temperature"]:
            pass

        for sensor in conf.sensor_configurations["level"]:
            pass