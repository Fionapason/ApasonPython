import configurations as conf

#TODO function to add all in_use sensors to the list

#TODO maybe make sensor in arduino an object of this one!

class Update_List_Pressure:

    name : str
    unit : str
    critical_pressure : float
    warning_pressure : float
    current_value : float

    def __init__(self, sensor):

        self.name = sensor["name"]
        self.unit = sensor["unit"]
        self.critical_pressure = sensor["critical_pressure"]
        self.warning_pressure = sensor["warning_pressure"]

    def updateValue (self, newPressure):
        self.current_value = newPressure
        return newPressure

class Sensor_Update_List:

    pressure = []

    def __init__(self):
        for sensor in conf.sensor_configurations["pressure"]: #will eventually need to be two for loops
            if sensor["in_use"]:
                new_Pressuresensor = Update_List_Pressure(sensor)
                self.pressure.append(new_Pressuresensor)

