import configurations as conf

#TODO function to add all in_use sensors to the list

class Update_List_Pressure:

    name : str
    unit : str
    critical_pressure : float
    warning_pressure : float
    current_value : float

    def __init__(self, sensor, arduino_sensor):

        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.critical_pressure = sensor["critical_pressure"]
        self.warning_pressure = sensor["warning_pressure"]
        self.arduino_pointer = arduino_sensor

    def updateValue (self, newPressure):
        self.current_value = newPressure
        return newPressure

class Update_List_Massflow:

    name : str
    unit : str
    current_value : float

    def __init__(self, sensor, arduino_sensor):

        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.arduino_pointer = arduino_sensor

    def updateValue (self, newMassflow):
        self.current_value = newMassflow
        return newMassflow

class Sensor_Update_List:

    pressure = []
    massflow = []

    def __init__(self, arduino_sensors):


        index = 0

        for sensor in conf.sensor_configurations["pressure"]: #will eventually need to be two for loops
            if sensor["in_use"]:
                new_pressure_sensor = Update_List_Pressure(sensor, arduino_sensors.pressure_sensors[index])
                self.pressure.append(new_pressure_sensor)
                index += 1

        index = 0

        for sensor in conf.sensor_configurations["massflow"]:
            if sensor["in_use"]:
                new_massflow_sensor = Update_List_Massflow(sensor, arduino_sensors.massflow_sensors[index])
                self.massflow.append(new_massflow_sensor)
                index += 1