import serial
import time


def readSerial(ser):
    buffer = ser.read().decode('utf-8')

    while (buffer == '') | (buffer == '\n') | (buffer == '\r') | (buffer == '\t'):
        time.sleep(0.05)
        ser.flush()
        buffer = ser.read().decode('utf-8')

    return buffer

#Function that makes sure that the serial port is properly communicating with the Arduino
#Prints 'Handshake Successful!' once the connection is secure
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

#Takes a serial port, an analog voltage reference, the maximum pressure of the pressure sensor and the maximum voltage it can return
#Returns the current pressure
def readPressure(ser, analogVoltageReference=1.1, maxPressure=30, maxVoltage=10):

    ser.flush()
    ser.write(b'v')
    #read string from serial port
    pressure = readSerial(ser)
    #convert string to float
    pressure = float(pressure)
    #convert float to the pressure
    pressure = pressure * analogVoltageReference * maxPressure / (1023*maxVoltage)

    ser.flush()

    return pressure



if __name__ == '__main__':

    system_running = int(input("Power on? 1/0" + '\n'))

    # initialize serial port usbmodem1401
    if system_running == 1:
        first_port = serial.Serial(port='/dev/tty.usbmodem1401', baudrate=115200, parity=serial.PARITY_NONE,
                                   bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=1, xonxoff=False,
                                   rtscts=False,
                                   dsrdtr=False)
        handshake(first_port)


    while system_running:
        choice = int(input("Do you want to check the pressure? 1/0" + '\n'))

        if choice == 1:
            print(readPressure(first_port))

        else:
            choice = int(input("Do you want to turn off the device? 1/0" + '\n'))
            if choice == 1:
                system_running = False
                print("Shutting down...")

    print("Power Off.")