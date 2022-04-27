import configurations as conf

analogReference = 5.0

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


class Pressure_Gems:

    commands = ['a']

    max_pressure: float

    def __init__(self, max):
        self.max_pressure = max



class Arduino_Sensors:

    pressure_commands = ['b', 'c', 'd', 'e']
    pressure_sensors = []

    def __init__(self):

        index = 0


        for sensor in conf.sensor_configurations["pressure"]:

            if sensor["in_use"]:

                current_command = bytes(self.pressure_commands[index], 'utf-8')
                new_pressure_sensor = Pressure(sensor["max_pressure"], current_command, index)
                self.pressure_sensors.append(new_pressure_sensor)
                index += 1


        #for loops for all the other sensor