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

    if count == maxLoops:
        print("COULDN'T FIND ARDUINO AT PORT: " + ser.port + "\n")
    else:
        print("PORT " + ser.port + " CONNECTED! \n")

    return


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
                                                        timeout=timeout_time, xonxoff=False, rtscts=False, dsrdtr=False)
            print("PORT OPENED \n")
            handshake(self.ports[arduino_counter])

            arduino_counter += 1

        return


def sendVoltage(ser, volt, port):

    if(port == 'A'):
        ser.write(b'!')
    elif(port == 'B'):
        ser.write(b'@')
    elif (port == 'C'):
        ser.write(b'#')
    elif (port == 'D'):
        ser.write(b'$')

    input_to_port = str(int( float(volt) / 5 * 4095))
    time.sleep(0.05)
    ser.write(bytes(input_to_port, 'utf-8'))
    return


if __name__ == '__main__':
    arduinos = talktoArduino()
