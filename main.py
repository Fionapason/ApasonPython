import serial
import time

# returns serial port input but ignores garbage
COMMAND_PRESSURE = b'v'
COMMAND_MASS_FLOW = b'i'


def readSerial(ser):
    buffer = ''

    while (buffer == '') | (buffer == '\n') | (buffer == '\r') | (buffer == '\t'):
        buffer = ser.read().decode('utf-8')
        time.sleep(0.05)
        ser.flush()

    return buffer


# Function that makes sure that the serial port is properly communicating with the Arduino
# Prints 'Handshake Successful!' once the connection is secure
def handshake(ser):
    # Handshake
    # flush port before starting
    ser.flush()

    # send an a and make sure we received an a
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
    return


# Takes a serial port, an analog voltage reference, the maximum pressure of the pressure sensor and the maximum
# voltage it can return Returns the current pressure
def readPressure(ser, analogVoltageReference=4.91, maxPressure=10, maxVoltage=10):
    ser.flush()
    ser.write(COMMAND_PRESSURE)
    # read from serial port
    msb = readSerial(ser)
    if float(msb) == 0:
        return 0
    middle = readSerial(ser)
    lsb = readSerial(ser)

    pressure = float(msb + middle + lsb + '')
    # convert float to the pressure
    pressure = pressure * analogVoltageReference * maxPressure / (1023 * maxVoltage)

    ser.flush()

    return pressure


def readMassflow(ser, analogVoltageReference=4.91, minMassflow=1, maxMassflow=20, minVoltage=0.88, maxVoltage=4.4,
                 graphConstant=-3.75):
    ser.flush()
    ser.write(COMMAND_MASS_FLOW)

    msb = readSerial(ser)
    if float(msb) == 0:
        return 0

    middle = readSerial(ser)
    lsb = readSerial(ser)

    massflow = float(msb + middle + lsb + '')

    massflow = massflow * (analogVoltageReference / 1023) * (
            (maxMassflow - minMassflow) / (maxVoltage - minVoltage)) + graphConstant

    ser.flush()

    return massflow


if __name__ == '__main__':

    system_running = int(input("Power on? 1/0" + '\n'))

    # initialize serial port usbmodem1401
    if system_running == 1:
        first_port = serial.Serial(port='/dev/tty.usbmodem1401', baudrate=115200, parity=serial.PARITY_NONE,
                                   bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=1, xonxoff=False,
                                   rtscts=False,
                                   dsrdtr=False)
        handshake(first_port)

    # process will need more sophistication later
    while system_running == 1:
        choice = int(input("Do you want to turn off the device, check the pressure, or the massflow? 0/1/2" + '\n'))

        if choice == 1:
            print(str(readPressure(first_port)) + " bar")
        elif choice == 2:
            print(str(readMassflow(first_port)) + " l/min")
        elif choice == 0:
            choice = int(input("Are you sure you want to turn off the device? 1/0" + '\n'))
            if choice == 1:
                system_running = False
                print("Shutting down...")
        else:
            print("ERROR. INVALID INPUT")

    print("Power Off.")
