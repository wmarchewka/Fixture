# this routine is used to program initiate TFP3 programmer
# via serial.  pass the serial port and action
import serial
import time

cyclone_recv1 = b'jP&E,14,Universal_PEMBC0F62,none,0,0,Dec 12 2016,9.80,Rev. A,00:0d:01:bc:0f:62,0,1,K70FN1M0_EMMC,ArmCortex,'
cyclone_recv2 = b'hP&E,14,Universal_PEMBC0F62,none,0,0,Dec 12 2016,9.80,Rev. A,00:0d:01:bc:0f:62,0,1,K70FN1M0_EMMC,Generic,'

#******************************************************************************************
def CycloneProgram(port):
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

# ******************************************************************************************
def TFP3Program(port):
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

#******************************************************************************************
def main():

    module = 'A'
    tmpPort = '/dev/tty.usbmodem14444321'

    if module == "A":
        ret = CycloneProgram(tmpPort)

    if module == "B":
        ret = TFP3Program(tmpPort)

    print(ret)



if __name__ == '__main__':
    main()