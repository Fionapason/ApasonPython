import time
import control_systems as control
import configurations_1 as conf_1
import configurations_2 as conf_2
import Sensor_Update_List as ul


"""
This class handles the current state of all apason control instruments and thus also sets the whole system into action.
Because of this, it also handles the control systems in a thread.

Upon initialization it adds every instrument to the corresponding class member list and also contains a function to turn
the instruments themselves on.

Each control instrument type has its own class with the members necessary for control.
It also has a for its type unique id, with which the command center thread will be able to send commands to the arduino.
Additionally, each control instrument keeps track of its state.

"""

# Parameters: id, name, state (float), max_RPM (float)
# Function: set_new_state(new_state)
class System_Pump:
    """
    **Parameters:** id, name, state (float), max_RPM (float) \n
    **Function:** set_new_state(new_state)
    """
    id : float
    name : str
    state : float
    changed = False
    max_RPM : float

    def __init__(self, id, max_RPM, name, state=0.0):

        self.state = state
        self.id = id
        self.name = name
        self.max_RPM = max_RPM

    def set_new_state(self, new_state):
        self.state = new_state
        self.changed = True

    def voltage_to_rpm(self, voltage):
        return voltage / 5.0 * self.max_RPM


# class System_PCV:
#
#     id : float
#     state : float
#     name : str
#     max_Opening = 100
#
#     def __init__(self, id, name, state=0):
#         self.id = id
#         self.name = name
#         self.state = state
#
#     def set_new_state(self, new_state):
#         self.state = new_state

# Parameters: id, name, state (str; "LOW" (eq. open) /"HIGH" (eq. closed)
# Function: set_new_state(new_state)
class System_OCV_NO:
    """
    **Parameters:** id, name, state (str; "LOW" (eq. open) /"HIGH" (eq. closed) \n
    **Function:** set_new_state(new_state)
    """
    id : float
    name : str
    state : str
    changed = False

    def __init__(self, id, name, state="LOW"):
        self.id = id
        self.name = name
        self.state = state

    def set_new_state(self, new_state):
        self.state = new_state
        self.changed = True

# Parameters: id, name, state (str; "LOW" (eq. closed) /"HIGH" (eq. open)
# Function: set_new_state(new_state)
class System_OCV_NC:
    """
    **Parameters:** id, name, state (str; "LOW" (eq. closed) /"HIGH" (eq. open) \n
    **Function:** set_new_state(new_state)
    """
    id : float
    name : str
    state : str
    changed = False

    def __init__(self, id, name, state="LOW"):
        self.id = id
        self.name = name
        self.state = state

    def set_new_state(self, new_state):
        self.state = new_state
        self.changed = True

# Parameters: id, name, state (str; "HIGH"/"LOW")
# Function: set_new_state(new_state)
class System_CV3:
    """
    **Parameters:** id, name, state (str; "HIGH"/"LOW")
    **Function:** set_new_state(new_state)
    """

    id: float
    name: str
    state : str
    changed = False

    def __init__(self, id, name, state="LOW"):
        self.id = id
        self.name = name
        self.state = state

    def set_new_state(self, new_state):
        self.state = new_state
        self.changed = True

# Parameters: state (str; "LOW"/"HIGH")
# Function: set_new_state(new_state)
class System_Polarity:
    """
    **Parameters:** state (str; "LOW"/"HIGH")
    **Function:** set_new_state(new_state)
    """
    state: str
    changed = False

    def __init__(self, state="OFF"):
        self.state = state

    def set_new_state(self, new_state):
        self.state = new_state
        self.changed = True

# Parameter: system_on = True, time_start (time.time()),
# lists for pumps, ocvs_no, ocvs_nc, cv3s
#Functions: turn_on_system(), turn_on_instruments(), turn_on_control()
class Apason_System():
    """
    **Parameter:** system_on = True, time_start (time.time()), \n
    lists for pumps, ocvs_no, ocvs_nc, cv3s \n
    **Functions:** turn_on_system(), turn_on_instruments(), turn_on_control(), set_instruments()
    """
    system_on = True

    system_pumps = []
    #system_pcvs = []
    system_ocvs_no = []
    system_ocvs_nc = []
    system_cv3s = []

    def turn_on_system(self, list):
        self.update_list = list
        if self.system_on:
            self.turn_on_instruments()
            self.time_start = time.time()
            self.turn_on_control()

    def turn_on_instruments(self):
        self.set_instruments()


    def turn_on_control(self):
        self.overall_control = control.Overall_Control(update_list=self.update_list, apason_system=self)

    def turn_off_system(self):
        self.overall_control.stop()

    def set_instruments(self):
        # Iterate through every pump in the configurations for the first arduino,
        # Create a new System_Pump, append it to system_pumps list
        for pump in conf_1.control_instrument_configurations_1["pump"]:
            # Make sure pump is in use
            if pump["in_use"]:
                new_pump = System_Pump(id=pump["id"],
                                       name=pump["name"],
                                       max_RPM=pump["max_RPM"],
                                       state=pump["starting_RPM"])
                self.system_pumps.append(new_pump)
        # for pcv in conf_1.control_instrument_configurations_1["pcv"]:
        #     if pcv["in_use"]:
        #         new_pcv = System_PCV(id=pcv["id"],
        #                              name=pcv["name"],
        #                              state=pcv["start_opening"])
        #         self.system_pcvs.append(new_pcv)

        for cv3 in conf_1.control_instrument_configurations_1["cv3"]:
            if cv3["in_use"]:
                new_cv3 = System_CV3(id=cv3["id"],
                                     name=cv3["name"],
                                     state=cv3["start_state"])
                self.system_cv3s.append(new_cv3)
        for ocv_no in conf_1.control_instrument_configurations_1["ocv_normally_open"]:
            if ocv_no["in_use"]:
                new_ocv_no = System_OCV_NO(id=ocv_no["id"],
                                           name=ocv_no["name"],
                                           state=ocv_no["start_state"])
                self.system_ocvs_no.append(new_ocv_no)
        for ocv_nc in conf_1.control_instrument_configurations_1["ocv_normally_closed"]:
            if ocv_nc["in_use"]:
                new_ocv_nc = System_OCV_NC(id=ocv_nc["id"],
                                           name=ocv_nc["name"],
                                           state=ocv_nc["start_state"])
                self.system_ocvs_nc.append(new_ocv_nc)


        # Second arduino
        for pump in conf_2.control_instrument_configurations_2["pump"]:
            if pump["in_use"]:
                new_pump = System_Pump(id=pump["id"],
                                       name=pump["name"],
                                       max_RPM=pump["max_RPM"],
                                       state=pump["starting_RPM"])
                self.system_pumps.append(new_pump)
        # for pcv in conf_2.control_instrument_configurations_2["pcv"]:
        #     if pcv["in_use"]:
        #         new_pcv = System_PCV(id=pcv["id"],
        #                              name=pcv["name"],
        #                              state=pcv["start_opening"])
        #         self.system_pcvs.append(new_pcv)
        for cv3 in conf_2.control_instrument_configurations_2["cv3"]:
            if cv3["in_use"]:
                new_cv3 = System_CV3(id=cv3["id"],
                                     name=cv3["name"],
                                     state=cv3["start_state"])
                self.system_cv3s.append(new_cv3)

        for ocv_no in conf_2.control_instrument_configurations_2["ocv_normally_open"]:
            if ocv_no["in_use"]:
                new_ocv_no = System_OCV_NO(id=ocv_no["id"],
                                           name=ocv_no["name"],
                                        state=ocv_no["start_state"])
                self.system_ocvs_no.append(new_ocv_no)

        for ocv_nc in conf_2.control_instrument_configurations_2["ocv_normally_closed"]:
            if ocv_nc["in_use"]:
                new_ocv_nc = System_OCV_NC(id=ocv_nc["id"],
                                           name=ocv_nc["name"],
                                           state=ocv_nc["start_state"])
                self.system_ocvs_nc.append(new_ocv_nc)

        for polarity in conf_2.control_instrument_configurations_2["polarity"]:
            if polarity["in_use"]:
                new_polarity = System_Polarity(state=polarity["start_state"])
                self.polarity = new_polarity





if __name__ == '__main__':
    update_list = ul.Sensor_Update_List()

    for sensor in update_list.pressure:
        sensor.updateValue(0)

    for sensor in update_list.massflow:
        sensor.updateValue(0)

    print(update_list.massflow[0].current_value)

    system_test = Apason_System()
    system_test.turn_on_system(update_list)

