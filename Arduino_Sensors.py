import configurations as conf

analogReference = 5.0

minVolt_current = 1.0

class Pressure_Gems:

    commands = ['a']

    max_pressure: float

    def __init__(self, max):
        self.max_pressure = max


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



class Arduino_Sensors:

    pressure_commands = ['b', 'c', 'd', 'e']
    pressure_sensors = []

    massflow_commands = ['f', 'g', 'h', 'i']
    massflow_sensors = []

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
