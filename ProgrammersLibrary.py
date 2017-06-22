# this routine is used to program initiate TFP3 programmer
# via serial.  pass the serial port and action
import serial
import time
import logging

logger = logging.getLogger()


cyclone_recv1 = b'jP&E,14,Universal_PEMBC0F62,none,0,0,Dec 12 2016,9.80,Rev. A,00:0d:01:bc:0f:62,0,1,K70FN1M0_EMMC,ArmCortex,'
cyclone_recv2 = b'hP&E,14,Universal_PEMBC0F62,none,0,0,Dec 12 2016,9.80,Rev. A,00:0d:01:bc:0f:62,0,1,K70FN1M0_EMMC,Generic,'

#******************************************************************************************
def CycloneProgram(self, port, image):
        # open com port wait for error
        #image selects what image in the programmer to select
        #if image =0 then select whatever is defaulted in the programmer

        if port ==  '':
            self.lblStatus.setText('Please select Cyclone serial port')
            return False, 'Please select Cyclone serial port'

        try:
            logger.debug('Looking for Cyclone programmer...')
            self.lblStatus.setText('Looking for Cyclone programmer...')
            time.sleep(1)
            ser = serial.Serial()#(port, 115200, timeout=1)
            ser.setRTS(False)           #needed to ensure the DTR or RTS line doesnt reset programmer on startup
            ser.setDTR(False)
            ser.baudrate = 115200
            ser.port = port
            ser.timeout = 1
            ser.open()
        except:
            logger.debug('Cyclone programmer not found...')
            self.lblStatus.setText('Cyclone programmer not found...')
            return False, 'Cyclone programmer not found...'
        # port found send commands to identify what it is
        self.lblStatus.setText('Programming Cyclone...')
        ser.write(b'\x03\x01\x18\x5d')          # first command
        logger.debug('SEND->\\x03\\x01\\x18\\x5d')     #
        line = ser.read(2)                      # response should be 01 00
        logger.debug('RECV->' + str(line))
        ser.write(b'\x03\x01\x0B\x24')  # write command
        logger.debug('SEND->\\x03\\x01\\x0B\\x24')
        line = ser.readline()
        logger.debug('RECV->' + str(line))
        if line == cyclone_recv1 or cyclone_recv2:
            logger.debug('RECV->' + str(line))
            if image==1:
                ser.write(b'\x04\x18\x1c\x01\x5f')  # command to select iamge 1
            if image==2:
                ser.write(b'\x04\x18\x1c\x02\x56')  # command to select iamge 2
            if image==3:
                ser.write(b'\x04\x18\x1c\x03\x51')  # command to select iamge 3
            if image==4:
                ser.write(b'\x04\x18\x1c\x04\x44')  # command to select iamge 4
            line = ser.readline()
            logger.debug('RECV->' + str(line))
            logger.debug('Cyclone programming Image ' +  str(image))
            self.lblStatus.setText('Cyclone programming Image ' +  str(image))
            ser.write(b'\x03\x18\x41\x3f')  # command to start programming
            logger.debug('SEND->\\x03\\x18\\x41\\x3f')
            line = ser.read(2)  # Check for new line and CR     # response should be 01 ee
            logger.debug('RECV->' + str(line))
            finished = False
            # repeat this asking for status until cyclone responds
            while not finished:
                ser.write(b'\x03\x18\x5f\x65')          # this is the command to start programming
                time.sleep(0.5)
                logger.debug('SEND->\\x03\\x18\\x5f\\x65')
                line = ser.readline()
                logger.debug('RECV->' + str(line))
                if line == b'\x03\x01\x01\xee':          #responce will be 03 00 00 ee until we recv a 03 01 01 ee
                    ser.write(b'\x03\x18\x33\x66')       # send to get status
                    logger.debug('SEND->\\x03\\x18\\x33\\x66')
                    line = ser.readline()
                    logger.debug('RECV->' + str(line))
                    if line == b'\x03\x00\x00\xee':
                        logger.debug('Cyclone Success')
                        ser.close()
                        return True, 'Cyclone Programmer Success'
                        self.lblStatus.setText('Cyclone Programmer Success')

                    else:
                        logger.debug("Error " + str(line[2]))
                        ser.close()
                        self.lblStatus.setText('Cyclone programmer failed. Error ' + str(line[2]))
                        return False, 'Cyclone programmer failed. Error ' + str(line[2])
        else:
            logger.debug('Did not find Cyclone programmer')
            self.lblStatus.setText('Did not find Cyclone programmer')
            return False, 'Did not find Cyclone Programmer'

# ******************************************************************************************
def TFP3Program(self, port):

    if port == '' or port == "None":
        self.lblStatus.setText('Please select TFP3 serial port')
        return False, 'Please select TFP3 serial port'

    try:

        logger.debug('Looking for TFP3 programmer on port' + port)
        self.lblStatus.setText('Looking for TFP3 programmer on port' + port)
        se = serial.Serial(port, 115200, timeout=5)
        logger.debug('se->' + str(se))
        logger.debug('Need to reset the programmer')
        se.write(b'z\r\n')
        logger.debug('Resetting programmer')
        self.lblStatus.setText('Resetting programmer')
        se.close()
        time.sleep(3)
        se.open()
        time.sleep(3)
        y = se.readall()
        z = str(y).find('Silergy flash programmer')
        logger.debug(y)
        if (z > -1):
            logger.debug('TFP3 programmer found')
            time.sleep(2)
            se.write(b'p\r\n')
            x = se.read_all()
            logger.debug("x->" +  str(x))
            se.close()
            # if x == b'Command Timeout\r\n':
            #     se.close()
            #     logger.debug('Command timeout. Did not find UUT')
            #     self.lblStatus.setText('Command timeout. Did not find UUT')
            #     return False, 'Command timeout. Did not find UUT'
            # else:
            #     logger.debug('TFP3 programmer found')
            #     self.lblStatus.setText('TFP3 programmer found')
            #     time.sleep(1)
            #     while True:
            #         time.sleep(0.001)
            #         n = se.inWaiting()
            #         if n:
            #             data = se.read(n)
            #             logger.debug(data)
            #             if data.find(b'Command Timeout') > -1:
            #                 logger.debug('UUT not found.  Timed out')
            #                 self.lblStatus.setText('UUT not found. Timed out')
            #                 return False, 'UUT not found.  TFP3 timeout programming'
            #             elif data.find(b'successful') > -1:
            #                 logger.debug('TFP3 program success')
            #                 self.lblStatus.setText('TFP3 program success')
            #                 return True, 'TFP3 program success'

        else:
            se.close()
            logger.debug("String not found Error")
            return False, 'Error'
    except Exception as err:
        se.close()
        self.lblStatus.setText(err)
        logger.debug(err)
        return False, err
#******************************************************************************************
def main():

    module = 'A'
    tmpPort = '/dev/tty.usbmodem14444321'

    if module == "A":
        ret = CycloneProgram(tmpPort)

    if module == "B":
        ret = TFP3Program(tmpPort)

    logger.debug(ret)



if __name__ == '__main__':
    main()
