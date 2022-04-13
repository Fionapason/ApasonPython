import serial
import time

timeout_time = 1

def readSerial(ser):

    maxLoops = timeout_time*1000
    buffer = ''
    count = 0

    while (ser.inWaiting() < 1) & (count < maxLoops) & ((buffer == '') | (buffer == '\n') | (buffer == '\r') | (buffer == '\t')) :
        time.sleep(0.001)
        count = count+1
        buffer = ser.read().decode('utf-8')


    while ser.inWaiting() > 0 :
        buffer = buffer + ser.read().decode('utf-8')

    ser.flush()

    return buffer

def handshake(ser):

    ser.flush()
    read = readSerial(ser)

    ser.write(b'a')

    count = 0
    maxLoops = timeout_time*1000
    read = readSerial(ser)

    while ("I AM DONE!" not in read) & (count < maxLoops):
        count += 1
        read = readSerial(ser)

    if count == maxLoops:
        print("COULDN'T FIND ARDUINO AT PORT: " + ser.port + "\n")
    else:
        print("PORT " + ser.port + " CONNECTED! \n")

    return


class talktoArduino:
    ports = dict()
    portnames = ['/dev/cu.usbmodem1401', '/dev/cu.usbmodem11301'] #, '/dev/cu.usbmodem11301'
    baud = 115200
    analogReference = 5

    def __init__(self):

        arduino_counter = 1

        for name in self.portnames:
            self.ports[arduino_counter] = serial.Serial(port=name, baudrate=self.baud, parity=serial.PARITY_NONE,
                                                        bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                                                        timeout=timeout_time, xonxoff=False, rtscts=False, dsrdtr=False)
            print("PORT OPENED \n")
            handshake(self.ports[arduino_counter])

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

        count = 0
        maxLoops = timeout_time * 1000

        read = readSerial(self.ports[id])

        while ('+' not in read) & (count < maxLoops):
            count += 1
            read = readSerial(self.ports[id])

        return

    def retrieveVoltage(self, id, COMMAND):

        self.ports[id].write(COMMAND)
        time.sleep(0.05)
        return readSerial(self.ports[id])


if __name__ == '__main__':

    arduinos = talktoArduino()


    arduinos.sendVoltage(1, 5, 'A')
    arduinos.sendVoltage(2, 2, 'A')
    print(arduinos.retrieveVoltage(1, b'b'))
    print(arduinos.retrieveVoltage(2, b'c'))