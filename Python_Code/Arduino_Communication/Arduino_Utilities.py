import serial
import time
import Configurations.Configurations_Arduino_UF as uf_conf
import Configurations.Configurations_Arduino_ED as ed_conf
from threading import Lock
from Arduino_Communication.Serial_Utilities import find_in_serial, read_serial, timeout_time


"""
This class contains a dictionary of all currently connected Arduinos.
Using the functions from Serial_Utilities, it establishes a connection with every Arduino port given in the configurations files.

The class also has functions it uses to retrieve and set both analog and digital signals,
which take a sensor/control instrument as a parameter, using its class members to identify, which command has to be sent to which Arduino,
as well as a Lock() object, which guarantees no interference between the threads of the system.

The functions check which Arduino the sensor is on and employ *two different Locks*, to maximize the programmes speed and not overkill the code protection.
"""

class Arduino_Utilities:
    '''**Parameters:** ports *dict()*, portnames *list*, baud, analog_reference, arduino_locks *list* \n
    **Functions:** handshake(serial), \n
    set_digital(control_instrument, state), set(lock, port, command)), \n
    check_digital(evel_switch), check(lock, port, command), \n
    send_voltage(volt, control_instrument, lock), send(control_instrument, lock, port, volt), \n
    retrieve_measurement(sensor, lock), retrieve(command, lock, port, sensor)
    '''
    ports = dict()
    port_names = []
    baud = 115200
    analog_reference = 5
    arduino_locks = [Lock(),Lock()]

    def __init__(self):
        arduino_counter = 1

        # Retrieve the Arduino port names from the configurations files
        self.port_names.append(uf_conf.port_name_arduino_uf)
        self.port_names.append(ed_conf.port_name_arduino_ed)

        # Establish a serial connection with both Arduinos
        for name in self.port_names:

            connection_problem = True

            while connection_problem:
                connection_problem = False
                self.ports[arduino_counter] = serial.Serial(port=name, baudrate=self.baud, parity=serial.PARITY_NONE,
                                                            bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                                                            timeout=timeout_time, xonxoff=False, rtscts=False, dsrdtr=False)
                print("PORT OPENED \n")

                if not self.handshake(self.ports[arduino_counter]):
                    print("There is a Connection Problem")
                    self.ports[arduino_counter].close()
                    connection_problem = True


            arduino_counter += 1

        return



    def handshake(self, serial):

        serial.flush()

        timeout_counter = 0

        # Ensure Arduino sent an a, send an a back until the timeout is reached.
        while (not find_in_serial(serial, 'a')) & (timeout_counter < 100):
            serial.write(b'a')
            timeout_counter += 1

        if timeout_counter >= 100:
            return False

        serial.write(b'a')

        if find_in_serial(serial, "I AM DONE!"):

            print("PORT " + serial.port + " CONNECTED! \n")

            # Checking if this is the UF Arduino and we need to send a signal to the UV lamp
            if serial.port == self.port_names[1]:

                # Turning on the UV lamp on the UF Arduino
                serial.write(b'(')
                find_in_serial(serial, '+')


            return True
        else:
            print("COULDN'T FIND ARDUINO AT PORT: " + serial.port + "\n")
        return

    # For valves and polarity
    def set_digital(self, control_instrument, state):

        arduino_id = control_instrument.arduino_id
        # find the lock corresponding to the Arduino, this instrument is plugged intp
        lock = self.arduino_locks[arduino_id - 1]
        port = self.ports[arduino_id]

        # retrieve the command from the control instrument
        if state == "HIGH":
            command = control_instrument.command_high
        elif state == "LOW":
            command = control_instrument.command_low
        elif state == "OFF":
            command = control_instrument.command_off
        else:
            command = bytes('a', 'utf-8')

        return self.set(lock=lock, port=port, command=command)

    def set(self, lock, port, command):
        # Starting Arduino dialogue, which must not be interrupted!
        lock.acquire()
        port.write(command)
        # the Arduino responds a plus once it has set the instrument.
        find_in_serial(port, '+')
        # Dialogue finished!
        lock.release()
        return

    # For levelswitches
    def check_digital(self, level_switch):

        arduino_id = level_switch.arduino_id
        lock = self.arduino_locks[arduino_id - 1]
        port = self.ports[arduino_id]
        command = level_switch.command
        return self.check(lock=lock, port=port, command=command)

    def check(self, lock, port, command):
        # Starting Arduino dialogue, which must not be interrupted!
        lock.acquire()
        port.write(command)
        time.sleep(0.05)
        level_switch_status = read_serial(port)
        lock.release()
        # Dialogue finished!
        if level_switch_status == '1':
            return 'CLOSED'
        elif level_switch_status == '0':
            return 'OPEN'

    # For Pumps
    def send_voltage(self, volt, control_instrument):

        arduino_id = control_instrument.arduino_id
        lock = self.arduino_locks[arduino_id - 1]
        port = self.ports[arduino_id]

        return self.send(control_instrument, lock, port, volt)

    def send(self, control_instrument, lock, port, volt):

        voltage = bytes(str(volt), 'utf-8')

        # Starting Arduino dialogue, which must not be interrupted!
        lock.acquire()

        if (control_instrument.DAC_output == 'A'):
            port.write(b'!')

        elif (control_instrument.DAC_output == 'B'):
            port.write(b'@')

        elif (control_instrument.DAC_output == 'C'):
            port.write(b'#')

        elif (control_instrument.DAC_output == 'D'):
            port.write(b'$')

        else:
            print("ERROR! DAC OUTPUT ARGUMENT MUST BE 'A', 'B', 'C', OR 'D'!")
            return

        time.sleep(0.05)

        port.write(voltage)
        # the Arduino responds a plus once it has set the instrument.
        find_in_serial(port, '+')

        # Dialogue finished!
        lock.release()

        return

    def retrieve_measurement(self, sensor):

        arduino_id = sensor.arduino_id
        lock = self.arduino_locks[arduino_id - 1]
        port = self.ports[arduino_id]
        command = sensor.command

        return self.retrieve(command, lock, port, sensor)

    def retrieve(self, command, lock, port, sensor):
        # Starting Arduino dialogue, which must not be interrupted!
        lock.acquire()

        port.write(command)
        time.sleep(0.05)
        raw_measurement = read_serial(port)

        lock.release()
        return sensor.current_value(raw_measurement)


