import time

timeout_time = 5

"""
This file contains a few functions created to simplify serial communication.
"""

def read_serial(ser):
    '''Reads strings of any length and stops when unwanted characters are reached'''
    maxLoops = timeout_time*1000
    buffer = ''
    count = 0

    while (ser.inWaiting() < 1) & (count < maxLoops) & \
            ((buffer == '') | (buffer == '\n') | (buffer == '\r') | (buffer == '\t') | (buffer == '-') ) :
        time.sleep(0.001)
        count = count+1
        buffer = ser.read().decode('utf-8')

    while ser.inWaiting() > 0 :
        buffer = buffer + ser.read().decode('utf-8')
        time.sleep(0.005)

    return buffer

def find_in_serial(ser, find):
    '''Checks if a specific string has been sent through the serial port, even if other characters are in it as well.'''
    count = 0
    maxLoops = timeout_time * 100
    read = read_serial(ser)

    while (find not in read) & (count < maxLoops):
        count += 1
        read = read_serial(ser)

    if count == maxLoops:
        return False
    else:
        return True


