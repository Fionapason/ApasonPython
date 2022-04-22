import serial
import time
import serialUtilities as ser
import configurations as conf

#TODO add lock
#TODO sensors belong here

class talktoArduino:
    ports = dict()
    portnames = ['/dev/cu.usbmodem1401'] #, '/dev/cu.usbmodem11301'
    baud = 115200
    analogReference = 5

    def __init__(self):

        arduino_counter = 1

        for name in self.portnames:
            self.ports[arduino_counter] = serial.Serial(port=name, baudrate=self.baud, parity=serial.PARITY_NONE,
                                                        bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                                                        timeout=ser.timeout_time, xonxoff=False, rtscts=False, dsrdtr=False)
            print("PORT OPENED \n")
            ser.handshake(self.ports[arduino_counter])

            arduino_counter += 1

        return


    def sendVoltage(self, id, volt, DAC_OUTPUT):

        if(DAC_OUTPUT == 'A'):
            self.ports[id].write(b'!')

        elif(DAC_OUTPUT == 'B'):
            self.ports[id].write(b'@')

        elif (DAC_OUTPUT == 'C'):
            self.ports[id].write(b'#')

        elif (DAC_OUTPUT == 'D'):
            self.ports[id].write(b'$')

        else:
            print("ERROR! DAC OUTPUT ARGUMENT MUST BE 'A', 'B', 'C', OR 'D'!")
            return

        input_to_port = str(int( float(volt) / 5 * 4095))
        time.sleep(0.05)
        self.ports[id].write(bytes(input_to_port, 'utf-8'))

        ser.findInSerial(self.ports[id], '+')

        return

    def retrieveMeasurement(self, id, sensor):

        self.ports[id].write(sensor.command)
        time.sleep(0.05)
        raw_measurement = ser.readSerial(self.ports[id])
        return sensor.currentValue(raw_measurement)


if __name__ == '__main__':

    arduinos = talktoArduino()


    arduinos.sendVoltage(1, 5, 'A')
    # arduinos.sendVoltage(2, 2, 'A')
    print(arduinos.retrieveMeasurement(1, b'b'))
    # print(arduinos.retrieveVoltage(2, b'c'))