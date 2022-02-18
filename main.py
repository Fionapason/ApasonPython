import serial
import time


def readSerial(ser):
    buffer = ser.read().decode('utf-8')

    while (buffer == '') | (buffer == '\n') | (buffer == '\r') | (buffer == '\t'):
        time.sleep(0.05)
        ser.flush()
        buffer = ser.read().decode('utf-8')

    return buffer


def handshake(ser):
    # Handshake
    # flush port before starting
    ser.flush()

    # send an a, make sure we received an a
    assert (readSerial(ser) == 'a')
    ser.write(b'a')
    ser.flush()

    # arduino sends a d when it has left the while loop in the handshake
    assert (readSerial(ser) == 'd')

    # Testing

    # Test 1
    ser.write(b'c')
    assert (readSerial(ser) == 'a')
    ser.flush()
    # Test 2
    ser.write(b'b')
    assert (readSerial(ser) == '0')
    ser.flush()
    # Test 3
    ser.write(b'9')
    assert (readSerial(ser) == '0')
    ser.flush()

    # Testing complete.
    print('Handshake Successful!')


if __name__ == '__main__':
    # initialize serial port usbmodem1401
    first_port = serial.Serial(port='/dev/tty.usbmodem1401', baudrate=115200, parity=serial.PARITY_NONE,
                               bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=1, xonxoff=False,
                               rtscts=False,
                               dsrdtr=False)

    handshake(first_port)
