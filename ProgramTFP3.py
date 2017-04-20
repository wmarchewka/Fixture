# this routine is used to program initiate TFP3 programmer
# via serial.  pass the serial port and action
import sys
import serial
import time


tmpPort = '/dev/tty.usbmodem14444321'

def main():
    #StartProgram(tmpPort)
    pass


def StartProgram(port):
    try:
        print('Trying to open port' + port)
        se =  serial.Serial(port, 115200)
        se.write(b'P\r\n')
        print('Writing P to programmer')
        x = se.read_until(terminator = b'Programming')
        print(x)
        if x != b'P\r\r\nProgramming':
            print('Did not find TFP3 programmer')
            return False,'TFP3 programmer not found'
        else:
            print('Found TFP3 programmer')
            while True:
                time.sleep(0.001)
                n = se.inWaiting()
                if n:
                    data = se.read(n)
                    print(data)
                    if data.find(b'Timeout') > -1:
                        print('TIMEOUT')
                        return False,'TFP3 timeout programming'
                    elif data.find(b'successful') > -1:
                        print('Success')
                        return True, 'TFP3 program success'
    except:
        return False,'Serial port error'
        print('Serial port error')


if __name__ == '__main__':
    main()
