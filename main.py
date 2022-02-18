import serial
import time


def readSerial(ser):
    buffer = ser.read().decode('utf-8')

    while (buffer == '') | (buffer == '\n') | (buffer == '\r') | (buffer == '\t'):
        time.sleep(0.05)
        ser.flush()
        buffer = ser.read().decode('utf-8')

    return buffer

#def testSerial(ser):
#check that a comes in response to c, 0 in response to b, use assertions


def handshake():

    ser = serial.Serial()
    ser.port = '/dev/tty.usbmodem1401'
    ser.baudrate = 115200
    ser.parity = serial.PARITY_NONE
    ser.bytesize = serial.EIGHTBITS
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False

    ser.open()
    ser.flush()

    text = ser.read().decode('utf-8')
    print(text)

    ser.write(b'a')
    ser.flush()

    print(readSerial(ser))

    ser.write(b'c')
    print(readSerial(ser))
    ser.flush()

    ser.write(b'b')
    print(readSerial(ser))
    ser.flush()

    ser.write(b'v')
    print(readSerial(ser))
    ser.flush()


if __name__ == '__main__':
    handshake()
    print('Done')
