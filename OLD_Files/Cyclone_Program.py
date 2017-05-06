import serial
import time
import QT_Project.mainwindow_auto as mw
cyclone_recv1 = b'jP&E,14,Universal_PEMBC0F62,none,0,0,Dec 12 2016,9.80,Rev. A,00:0d:01:bc:0f:62,0,1,K70FN1M0_EMMC,ArmCortex,'
cyclone_recv2 = b'hP&E,14,Universal_PEMBC0F62,none,0,0,Dec 12 2016,9.80,Rev. A,00:0d:01:bc:0f:62,0,1,K70FN1M0_EMMC,Generic,'

def Cyclone():
    def ProgramCyclone(port):
        # open com port wait for error
        try:
            print('Looking for scanner...')
            ser = serial.Serial(port, 115200, timeout=1)
        except:
            print('Cyclone error...')
            return False, "Com Error"
        # port found send commands to identify what it is
        ser.write(b'\x03\x01\x18\x5d')          # first command
        print('SEND->\\x03\\x01\\x18\\x5d')     #
        line = ser.read(2)                      # response should be 01 00
        print('RECV->' + str(line))
        ser.write(b'\x03\x01\x0B\x24')  # write command
        print('SEND->\\x03\\x01\\x0B\\x24')
        line = ser.readline()
        print('RECV->' + str(line))
        if line == cyclone_recv1 or cyclone_recv2:
            print('RECV->' + str(line))
            print('Found Cyclone programmer')
            ser.write(b'\x03\x18\x41\x3f')  # command to start programming
            print('SEND->\\x03\\x18\\x41\\x3f')
            line = ser.read(2)  # Check for new line and CR     # response should be 01 ee
            print('RECV->' + str(line))
            finished = False
            # repeat this asking for status until cyclone responds
            while not finished:
                ser.write(b'\x03\x18\x5f\x65')          # this is the command to start programming
                time.sleep(0.5)
                print('SEND->\\x03\\x18\\x5f\\x65')
                line = ser.readline()
                print('RECV->' + str(line))
                if line == b'\x03\x01\x01\xee':          #responce will be 03 00 00 ee until we recv a 03 01 01 ee
                    ser.write(b'\x03\x18\x33\x66')       # send to get status
                    print('SEND->\\x03\\x18\\x33\\x66')
                    line = ser.readline()
                    print('RECV->' + str(line))
                    if line == b'\x03\x00\x00\xee':
                        print('Cyclone Success')
                        ser.close()
                        return True, 'Cyclone Programmer Success'
                    else:
                        print("Error " + str(line[2]))
                        ser.close()
                        return False, 'Cyclone programmer failed. Error ' + str(line[2])
        else:
            print('Did not find Cyclone programmer')
            return False, 'Did not find Cyclone Programmer'


def __init__(self):
    super().__init__()
    self.initUI()


def main():
    tmp_port='/dev/ttyUSB0'
    ret = Cyclone.ProgramCyclone(tmp_port)
    print(ret)



if __name__ == '__main__':
    main()


