import configurations as conf

analogReference = 5.0

minVolt_current = 1.0

#TODO TEST ALL OF THESE

class Pressure:

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

class Massflow:

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


class Conductivity:

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

class Temperature:

    command : str

    graph_constant : float

    max_temp : float

    min_temp : float

    arduino_id : int

    id : int

    def __init__(self, max, command, arduino_id, id):
        self.max_temp = max
        self.min_temp = 0
        self.command = command
        self.id = id
        self.arduino_id = arduino_id
        self.graph_constant = self.max_temp - ((self.max_temp - self.min_temp) / (analogReference - minVolt_current)) * analogReference


    def currentValue(self, raw_measurement):
        return float(raw_measurement) * (analogReference / 1023.0) * (self.max_temp - self.min_temp) / (analogReference - minVolt_current) + self.graph_constant

class Switch:
    command: str

    arduino_id : int

    id : int

    def __init__(self, command, arduino_id, id):
        self.command = command
        self.id = id
        self.arduino_id = arduino_id


class Arduino_Sensors:


    pressure_commands = ['a', 'b', 'c', 'd', 'e']
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

        for sensor in conf.sensor_configurations["pressure"]:

            if sensor["in_use"]:

                index = sensor["id"]

                current_command = bytes(self.pressure_commands[index], 'utf-8')
                new_pressure_sensor = Pressure(max=sensor["max_pressure"],
                                               command=current_command,
                                               id=index,
                                               arduino_id=sensor["arduino_id"])
                self.pressure_sensors.append(new_pressure_sensor)

        for sensor in conf.sensor_configurations["massflow"]:

            index = sensor["id"]

            if sensor["in_use"]:
                current_command = bytes(self.massflow_commands[index], 'utf-8')
                new_massflow_sensor = Massflow(max=sensor["max_flow"],
                                               command=current_command,
                                               id=index,
                                               arduino_id=sensor["arduino_id"])
                self.massflow_sensors.append(new_massflow_sensor)

        for sensor in conf.sensor_configurations["conductivity"]:

            index = sensor["id"]

            if sensor["in_use"]:
                current_command = bytes(self.conductivity_commands[index], 'utf-8')
                new_conductivity_sensor = Conductivity(max=sensor["max_Cond"],
                                                       min=sensor["min_Cond"],
                                                       command=current_command,
                                                       id=index,
                                                       arduino_id=sensor["arduino_id"])
                self.conductivity_sensors.append(new_conductivity_sensor)

        for sensor in conf.sensor_configurations["temperature"]:

            index = sensor["id"]

            if sensor["in_use"]:
                current_command = bytes(self.temperature_commands[index], 'utf-8')
                new_temperature_sensor = Temperature(max=sensor["max_Temp"],
                                                      command=current_command, id=index,
                                                      arduino_id=sensor["arduino_id"])
                self.temperature_sensors.append(new_temperature_sensor)

        for sensor in conf.sensor_configurations["level"]:

            index = sensor["id"]

            if sensor["in_use"]:
                current_command = bytes(self.levelswitch_commands[index], 'utf-8')
                new_level_switch = Switch(command=current_command,
                                          id=index,
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

    for sensor in try_list.temperature_sensors:
        print(sensor.id)

    for sensor in try_list.levelswitch_sensors:
        print(sensor.id)
