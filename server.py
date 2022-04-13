import talktoArduino as talk

if __name__ == '__main__':

    arduinos = talk.talktoArduino()
    arduinos.sendVoltage(1, 3, 'A')

