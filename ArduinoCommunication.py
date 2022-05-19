import serial
import time
import serialUtilities as ser
from threading import Lock

"""
This class contains a dictionary of all currently connected arduinos.
Using the functions from serialUtilities, it establishes a connection with every arduino port from the port_names list.

The class also has two functions: retrieveMeasurement and sendVoltage,
which take a sensor/control instrument as a parameter, using its class members to identify, which command has to be sent to which arduino,
as well as a lock object, which guarantees no interference between the threads of the system.
sendVoltage also takes the needed value from 0-4095 to be sent to the appropriate DAC output, also found by the member of the class
"""

class ArduinoCommunication:
    '''**Parameters:** ports *dict()*, portnames *list* \n
    **Functions:** sendVoltage(volt, control_instrument, lock), retrieveMeasurement(sensor, lock)
    '''
    ports = dict()
    port_names = ['/dev/cu.usbmodem1401', '/dev/cu.usbmodem1201'] #, '/dev/cu.usbmodem1201'
    baud = 115200
    analogReference = 5
    arduino_locks = [Lock(),Lock()]

    def __init__(self):
        arduino_counter = 1

        for name in self.port_names:

            connection_problem = True

            while connection_problem:
                connection_problem = False
                self.ports[arduino_counter] = serial.Serial(port=name, baudrate=self.baud, parity=serial.PARITY_NONE,
                                                            bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                                                            timeout=ser.timeout_time, xonxoff=False, rtscts=False, dsrdtr=False)
                print("PORT OPENED \n")

                if not ser.handshake(self.ports[arduino_counter]):
                    print("There is a Connection Problem")
                    self.ports[arduino_counter].close()
                    connection_problem = True


            arduino_counter += 1

        return

    def setDigital(self, control_instrument, state):
        arduino_id = control_instrument.arduino_id
        lock = self.arduino_locks[arduino_id - 1]
        port = self.ports[arduino_id]
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
        lock.acquire()
        port.write(command)
        ser.findInSerial(port, '+')
        lock.release()
        return

    def checkDigital(self, level_switch):

        arduino_id = level_switch.arduino_id
        lock = self.arduino_locks[arduino_id - 1]
        port = self.ports[arduino_id]
        command = level_switch.command
        return self.check(lock=lock, port=port, command=command)

    def check(self, lock, port, command):
        lock.acquire()
        port.write(command)
        time.sleep(0.05)
        level_switch_status = ser.readSerial(port)
        lock.release()
        if level_switch_status == '1':
            return 'CLOSED'
        elif level_switch_status == '0':
            return 'OPEN'

    def sendVoltage(self, volt, control_instrument):

        arduino_id = control_instrument.arduino_id
        lock = self.arduino_locks[arduino_id - 1]
        port = self.ports[arduino_id]

        return self.send(control_instrument, lock, port, volt)

    def send(self, control_instrument, lock, port, volt):

        voltage = bytes(str(volt), 'utf-8')
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
        ser.findInSerial(port, '+')
        lock.release()
        return

    def retrieveMeasurement(self, sensor):

        arduino_id = sensor.arduino_id
        lock = self.arduino_locks[arduino_id - 1]
        port = self.ports[arduino_id]
        command = sensor.command

        return self.retrieve(command, lock, port, sensor)

    def retrieve(self, command, lock, port, sensor):
        lock.acquire()
        port.write(command)
        time.sleep(0.05)
        raw_measurement = ser.readSerial(port)
        lock.release()
        return sensor.currentValue(raw_measurement)


    # def old_sendVoltage(self, id, volt, DAC_OUTPUT, lock):
    #
    #     lock.acquire()
    #
    #     if(DAC_OUTPUT == 'A'):
    #         self.ports[id].write(b'!')
    #
    #     elif(DAC_OUTPUT == 'B'):
    #         self.ports[id].write(b'@')
    #
    #     elif (DAC_OUTPUT == 'C'):
    #         self.ports[id].write(b'#')
    #
    #     elif (DAC_OUTPUT == 'D'):
    #         self.ports[id].write(b'$')
    #
    #     else:
    #         print("ERROR! DAC OUTPUT ARGUMENT MUST BE 'A', 'B', 'C', OR 'D'!")
    #         return
    #
    #     input_to_port = str(int( float(volt) / 5 * 4095))
    #     time.sleep(0.05)
    #     self.ports[id].write(bytes(input_to_port, 'utf-8'))
    #
    #     ser.findInSerial(self.ports[id], '+')
    #
    #     lock.release()
    #
    #     return


if __name__ == '__main__':
    pass
    # arduinos = ArduinoCommunication()
    #
    # lock = Lock()
    #
    # arduinos.sendVoltage(1, 5, 'A')
    # arduinos.sendVoltage(2, 2, 'A')
    # print(arduinos.retrieveMeasurement(1, b'b'))
    # print(arduinos.retrieveVoltage(2, b'c'))