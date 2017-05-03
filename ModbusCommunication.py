import minimalmodbus
import time

def mbComm(comport, address, register):

    try:
        uut = minimalmodbus.Instrument(comport, address)
        uut.debug = True
        uut.serial.timeout = 5.0
        uut.serial.bytesize = 8
        uut.serial.parity  = minimalmodbus.serial.PARITY_EVEN
        uut.serial.baudrate = 19200
        uut.serial.stopbits = 1
        uut.mode = minimalmodbus.MODE_RTU
        uut.close_port_after_each_call = False
        count = 0
        while count < 100:
            value = uut.read_register(register, 1, 4)     #register, number of decimals
            #value = uut.read_float(register)  # register, number of decimals
            print('Value->' + str(value))
            time.sleep(2.0)
            count = count + 1
        uut.serial.close
        return True, "Success"

    except OSError as err:
        print(err)
        return False, err

    except IOError as err1:
        print(err1)
        return False, err1

    except ValueError as err2:
        print(err2)
        return False , err2


def __init__(self):
    super().__init__()
    self.initUI()

def main():
    add = 1
    #comport = 'COM44'
    comport = '/dev/tty.usbserial-FT084UEL'
    register = 490
    register = 19
    ret = mbComm(comport, add, register)
    print(ret)

if __name__ == '__main__':
    main()
