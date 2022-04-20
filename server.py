import talktoArduino as talk
import configurations as conf
import sensors as sens
import kivy as UI


if __name__ == '__main__':

    arduinos = talk.talktoArduino()

    check_configurations = conf.check_configurations
    set_configurations = conf.set_configurations

