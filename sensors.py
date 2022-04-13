class Sensors:

    def __init__(self, configurations, types, sensors, ):

        self.configurations = configurations
        self.types = types
        self.sensors = []

        for type in types:
            self.sensors.append(type)
            type.

