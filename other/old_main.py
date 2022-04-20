import serial
import time

# returns serial port input but ignores garbage
COMMAND_WRITE_VOLTAGE = b'm'
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
    assert (readSerial(ser) == 'E')
    ser.flush()

    # Test 2
    ser.write(b'b')
    assert (readSerial(ser) == '0')
    assert (readSerial(ser) == 'E')
    ser.flush()

    # Test 3
    ser.write(b'9')
    assert (readSerial(ser) == '0')
    assert (readSerial(ser) == 'E')
    ser.flush()

    # Testing complete.
    print('Handshake Successful!')
    return


# Takes a serial port, an analog voltage reference, the maximum pressure of the pressure sensor and the maximum
# voltage it can return Returns the current pressure
def readPressure(ser, analogVoltageReference=5, maxPressure=10, maxVoltage=10):
    ser.flush()
    ser.write(COMMAND_PRESSURE)

    # read from serial port
    bit_list = []
    condition = True
    while(condition):
        current = readSerial(ser)
        if (current == 'E'):
            break
        bit_list.append(current)

    pressure = int(''.join(bit_list))

    pressure = pressure * 2

    # convert float to the pressure
    pressure = pressure * analogVoltageReference * maxPressure / (1023 * maxVoltage)

    ser.flush()

    return pressure


def readMassflow(ser, analogVoltageReference=5, minMassflow=1, maxMassflow=20, minVoltage=0.88, maxVoltage=4.4,
                 graphConstant=-3.75):
    try:
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

        return massflow
    finally:
        ser.flush()


# voltage must be between 0 and 5 !
def writeVoltage(ser, volt, analogVoltageReference=5):
    ser.flush()
    ser.write(COMMAND_WRITE_VOLTAGE)

    time.sleep(0.1)

    input_to_port = int(float(volt) / analogVoltageReference * 4096)
    print(input_to_port)
#    print(input_to_port.to_bytes(2, "big"))
    digits = [int(x) for x in str(input_to_port)]

    digit_amount = len(digits)
    digits = bytearray(digits)
    count = 0

    ser.write(digit_amount)
    time.sleep(0.01)
    ser.write(input_to_port)

    # while (digit_amount > count):
    #     current = digits[digit_amount - 1 - count]
    #     current = current.to_bytes(1,"big")
    #     ser.write(current)
    #     time.sleep(0.05)
    #     count += 1

    print(readSerial(ser))
    print(readSerial(ser))
    print(readSerial(ser))
    print(readSerial(ser))

    return


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
        choice = int(input("Do you want to turn off the device, check the pressure, check the massflow, or set a "
                           "Voltage? 0/1/2/3" + '\n'))

        if choice == 1:
            print(str(readPressure(first_port)) + " bar")
        elif choice == 2:
            print(str(readMassflow(first_port)) + " l/min")
        elif choice == 3:
            voltage = input("What voltage do you want? (DO NOT EXCEED 5!)" + '\n')
            writeVoltage(first_port, voltage)
            print("SUCCESS!")
        elif choice == 0:
            choice = int(input("Are you sure you want to turn off the device? 1/0" + '\n'))
            if choice == 1:
                system_running = False
                print("Shutting down...")
        else:
            print("ERROR. INVALID INPUT")

    print("Power Off.")