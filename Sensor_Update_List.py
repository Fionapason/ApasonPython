import configurations as conf

#TODO function to add all in_use sensors to the list

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

class Sensor_Update_List:

    lst = []

    def __init__(self):
        for sensor in conf.sensor_configurations["pressure"]: #will eventually need to be two for loops
            if sensor["in_use"]:
                new_Pressuresensor = Update_List_Pressure(sensor)
                self.lst.append(new_Pressuresensor)

