import minimalmodbus
import time

def mbComm(comport,address):

    try:


        uut = minimalmodbus.Instrument(comport, address)
        uut.debug = True
        uut.serial.timeout = 0.5
        uut.serial.bytesize = 8
        uut.serial.parity  = minimalmodbus.serial.PARITY_NONE
        uut.serial.baudrate = 19200
        uut.serial.stopbits = 1
        uut.mode = minimalmodbus.MODE_RTU
        count = 0
        while count < 5:
            value = uut.read_register(19, 1 , 4)     #register, number of decimals
            print('Value->' + str(value))
            time.sleep(1)
            count = count + 1
            #uut.write_register(24, 450, 1)
            #uut.read_register(24, 1)
        return True

    except OSError as err:
        print(err)
        return False, err

    except IOError as err1:
        print(err1)
        return False,err1


def __init__(self):
    super().__init__()
    self.initUI()

def main():
    add = 1
    comport = 'COM44'
    ret = mbComm(comport, add)
    print(ret)

if __name__ == '__main__':
    main()
