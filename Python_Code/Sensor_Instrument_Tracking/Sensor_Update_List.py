from Configurations import Configurations_Arduino_ED as conf_2, Configurations_Arduino_UF as conf_1

"""
This is a class, which contains a lists of all the sensors,
which will be used to easily display their values in the GUI and also for the control system to keep track of.

Every sensor within the lists is an instance of its own class type.

A class instance contains general information, like the specific sensor's name, the unit of measurement it uses,
the unique id, which it has in common with the Arduino_Sensor object, and the current measurement.
It may also have specific unique parameters.
It gets these parameters from the configurations files.

It can receive a new current_value via the update_value(self, newValue) function.
"""


class Update_List_Pressure:
    '''**Parameters:** name, unit, id, current_value, critical_pressure, warning_pressure \n
    **Function:** updateValue'''

    name: str
    unit: str
    critical_pressure: float
    warning_pressure: float
    current_value: float
    average_count = 3
    id: int

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.critical_pressure = sensor["critical_pressure"]
        self.warning_pressure = sensor["warning_pressure"]
        self.id = sensor["id"]
        self.average = []
        self.update_value(1.0)

    def update_value(self, newValue):

        # We use an average of the past three measurements, so that overshoots are ignored

        if len(self.average) == self.average_count:
            self.average.pop(0)
        self.average.append(newValue)
        self.current_value = sum(self.average) / len(self.average)
        return self.current_value


class Update_List_Massflow:
    '''**Parameters:** name, unit, id, current_value, \n
    **Function:** updateValue'''

    name: str
    unit: str
    current_value: float
    average_count = 3
    id: float

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.id = sensor["id"]
        self.average = []
        self.update_value(0.0)

    def update_value(self, newValue):
        # We use an average of the past three measurements, so that overshoots are ignored

        if len(self.average) == self.average_count:
            self.average.pop(0)
        self.average.append(newValue)
        self.current_value = sum(self.average) / len(self.average)
        return self.current_value



class Update_List_Conductivity:
    '''**Parameters:** name, unit, id, current_value \n
    **Function:** updateValue'''
    name: str
    unit: str
    current_value: float
    average_count = 3
    id: float

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.id = sensor["id"]
        self.average = []
        self.update_value(0.0)

    def update_value(self, newValue):
        # We use an average of the past three measurements, so that overshoots are ignored
        if len(self.average) == self.average_count:
            self.average.pop(0)
        self.average.append(newValue)
        self.current_value = sum(self.average) / len(self.average)
        return self.current_value

class Update_List_LevelSwitch:
    '''**Parameters:** name, id, current_value \n
    **Function:** updateValue'''
    name: str
    current_value: str
    id: float

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.id = sensor["id"]

    def update_value(self, newState):
        self.current_value = newState
        return newState




class Sensor_Update_List:
    '''**Parameters:** *lists:* pressure, massflow, conductivity, temperature, levelswitch'''
    pressure = []
    massflow = []
    conductivity = []
    # temperature = []
    levelswitch = []


    def __init__(self):

        # Iterate through all sensors of one type
        for sensor in conf_1.sensor_configurations_uf["pressure"]:
            # Check if sensor is in use
            if sensor["in_use"]:
                # Initiate new sensor
                new_pressure_sensor = Update_List_Pressure(sensor)
                # Append new sensor to the list
                self.pressure.append(new_pressure_sensor)

        for sensor in conf_1.sensor_configurations_uf["massflow"]:
            if sensor["in_use"]:
                new_massflow_sensor = Update_List_Massflow(sensor)
                self.massflow.append(new_massflow_sensor)

        index = 0
        for sensor in conf_1.sensor_configurations_uf["conductivity"]:
            if sensor["in_use"]:
                new_conductivity_sensor = Update_List_Conductivity(sensor)
                self.conductivity.append(new_conductivity_sensor)


        for sensor in conf_1.sensor_configurations_uf["level"]:
            if sensor["in_use"]:
                new_levelswitch_sensor = Update_List_LevelSwitch(sensor)
                self.levelswitch.append(new_levelswitch_sensor)

        # Repeat for sensors on 2nd arduino
        for sensor in conf_2.sensor_configurations_ed["pressure"]:
            if sensor["in_use"]:
                new_pressure_sensor = Update_List_Pressure(sensor)
                self.pressure.append(new_pressure_sensor)

        for sensor in conf_2.sensor_configurations_ed["massflow"]:
            if sensor["in_use"]:
                new_massflow_sensor = Update_List_Massflow(sensor)
                self.massflow.append(new_massflow_sensor)

        for sensor in conf_2.sensor_configurations_ed["conductivity"]:
            if sensor["in_use"]:
                new_conductivity_sensor = Update_List_Conductivity(sensor)
                self.conductivity.append(new_conductivity_sensor)
                index += 1


        for sensor in conf_2.sensor_configurations_ed["level"]:
            if sensor["in_use"]:
                new_levelswitch_sensor = Update_List_LevelSwitch(sensor)
                self.levelswitch.append(new_levelswitch_sensor)
