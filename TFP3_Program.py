# this routine is used to program initiate TFP3 programmer
# via serial.  pass the serial port and action
import sys
import serial
import time





def main():
    tmpPort = '/dev/tty.usbmodem1444441'
    tmpPort = '/dev/ttyACM1'
    ret = StartProgram(tmpPort)
    print(ret)
    pass


def StartProgram(port):
    try:
        print('Trying to open port' + port)
        se =  serial.Serial(port, 115200,timeout=5)
        se.write(b'P\r')
        while True:
            x = se.readline()
            print(x)
            if x == b'Programming target flash...\r\n':
                while True:
                    x = se.readline()
                    print(x)
                    if x == b'Program operation successful\r\n':
                        print(x)
                        return True, x
                    if x == b'Command Timeout\r\n':
                        print(x)
                        return False, x

    except:
        print('Serial port error')
        return False,'Serial port error'


if __name__ == '__main__':
    main()
