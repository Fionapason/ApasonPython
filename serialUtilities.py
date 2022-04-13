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

    return buffer

def findInSerial(ser, find):

    count = 0
    maxLoops = timeout_time * 1000
    read = readSerial(ser)

    while (find not in read) & (count < maxLoops):
        count += 1
        read = readSerial(ser)

    if count == maxLoops:
        return False
    else:
        return True

def handshake(ser):

    ser.flush()

    findInSerial(ser, 'a')
    ser.write(b'a')

    if findInSerial(ser, "I AM DONE!"):
        print("PORT " + ser.port + " CONNECTED! \n")
    else:
        print("COULDN'T FIND ARDUINO AT PORT: " + ser.port + "\n")

    return
