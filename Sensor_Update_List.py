# TODO TEST ALL OF THESE

import configurations_1 as conf_1
import configurations_2 as conf_2

"""
This is a class, which contains a lists of all the sensors,
which will be used to easily display their values in the GUI.

Every sensor within the lists is an instance of its own class type.

A class instance contains general information, like the specific sensor's name, the unit of measurement it uses,
the unique id, which it has in common with the Arduino_Sensor object, and the current measurement.
It may also have specific unique parameters.
It gets these parameters from the configurations files.

It can receive a new currentValue via the updateValue(self, newValue) function.
"""


# Parameters: name, unit, id, current_value, critical_pressure, warning_pressure
# Function: updateValue

class Update_List_Pressure:
    '''**Parameters:** name, unit, id, current_value, critical_pressure, warning_pressure \n
    **Function:** updateValue'''

    name: str
    unit: str
    critical_pressure: float
    warning_pressure: float
    current_value: float
    id: int

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.critical_pressure = sensor["critical_pressure"]
        self.warning_pressure = sensor["warning_pressure"]
        self.id = sensor["id"]

    def updateValue(self, newPressure):
        self.current_value = newPressure
        return newPressure


# Parameters: name, unit, id, current_value
# Function: updateValue

class Update_List_Massflow:
    '''**Parameters:** name, unit, id, current_value, \n
    **Function:** updateValue'''

    name: str
    unit: str
    current_value: float
    id: float

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.id = sensor["id"]

    def updateValue(self, newMassflow):
        self.current_value = newMassflow
        return newMassflow


# Parameters: name, unit, id, current_value
# Function: updateValue

class Update_List_Conductivity:
    '''**Parameters:** name, unit, id, current_value \n
    **Function:** updateValue'''
    name: str
    unit: str
    current_value: float
    id: float

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.id = sensor["id"]

    def updateValue(self, newConductivity):
        self.current_value = newConductivity
        return newConductivity


# Parameters: name, unit, id, current_value
# Function: updateValue

class Update_List_Temperature:
    '''**Parameters:** name, unit, id, current_value \n
    **Function:** updateValue'''
    name: str
    unit: str
    current_value: float
    id: float

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.id = sensor["id"]

    def updateValue(self, newTemperature):
        self.current_value = newTemperature
        return newTemperature


# Parameters: name, unit, id, current_value
# Function: updateValue

class Update_List_LevelSwitch:
    '''**Parameters:** name, id, current_value \n
    **Function:** updateValue'''
    name: str
    current_value: str
    id: float

    def __init__(self, sensor):
        self.name = sensor["name"]
        self.id = sensor["id"]

    def updateValue(self, newState):
        self.current_value = newState
        return newState


# Contains all the lists for every sensor type
# Parameters: pressure, massflow, conductivity, temperature, levelswitch

class Sensor_Update_List:
    '''**Parameters:** *lists:* pressure, massflow, conductivity, temperature, levelswitch'''
    pressure = []
    massflow = []
    conductivity = []
    temperature = []
    levelswitch = []


    def __init__(self):

        # Iterate through all sensors of one type
        for sensor in conf_1.sensor_configurations_1["pressure"]:
            # Check if sensor is in use
            if sensor["in_use"]:
                # Initiate new sensor
                new_pressure_sensor = Update_List_Pressure(sensor)
                # Append new sensor to the list
                self.pressure.append(new_pressure_sensor)

        for sensor in conf_1.sensor_configurations_1["massflow"]:
            if sensor["in_use"]:
                new_massflow_sensor = Update_List_Massflow(sensor)
                self.massflow.append(new_massflow_sensor)

        for sensor in conf_1.sensor_configurations_1["conductivity"]:
            if sensor["in_use"]:
                new_conductivity_sensor = Update_List_Conductivity(sensor)
                self.conductivity.append(new_conductivity_sensor)

        for sensor in conf_1.sensor_configurations_1["temperature"]:
            if sensor["in_use"]:
                new_temperature_sensor = Update_List_Temperature(sensor)
                self.temperature.append(new_temperature_sensor)

        for sensor in conf_1.sensor_configurations_1["level"]:
            if sensor["in_use"]:
                new_levelswitch_sensor = Update_List_LevelSwitch(sensor)
                self.levelswitch.append(new_levelswitch_sensor)

        # Repeat for sensors on 2nd arduino
        for sensor in conf_2.sensor_configurations_2["pressure"]:
            if sensor["in_use"]:
                new_pressure_sensor = Update_List_Pressure(sensor)
                self.pressure.append(new_pressure_sensor)

        for sensor in conf_2.sensor_configurations_2["massflow"]:
            if sensor["in_use"]:
                new_massflow_sensor = Update_List_Massflow(sensor)
                self.massflow.append(new_massflow_sensor)

        for sensor in conf_2.sensor_configurations_2["conductivity"]:
            if sensor["in_use"]:
                new_conductivity_sensor = Update_List_Conductivity(sensor)
                self.conductivity.append(new_conductivity_sensor)

        for sensor in conf_2.sensor_configurations_2["temperature"]:
            if sensor["in_use"]:
                new_temperature_sensor = Update_List_Temperature(sensor)
                self.temperature.append(new_temperature_sensor)

        for sensor in conf_2.sensor_configurations_2["level"]:
            if sensor["in_use"]:
                new_levelswitch_sensor = Update_List_LevelSwitch(sensor)
                self.levelswitch.append(new_levelswitch_sensor)
