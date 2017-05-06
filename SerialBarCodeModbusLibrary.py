import glob
import time
import sys

import minimalmodbus
import serial

from OLD_Files import Configuration as cf, Logfile as lf


#******************************************************************************************
def collectSerialPorts():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    print("Searching for serial ports...")
    settings = []
    for port in ports:
        try:
            s = serial.Serial(port)
            #st = s.get_settings()
            s.close()
            settings.append(port)
            print('Found->' + port)
        except (OSError, serial.SerialException):
            pass
    settings.append('none')
    return settings

#******************************************************************************************
def MajorBoardType(p_number, board_type, config_cal):
    global major_board_type
    global board_voltage
    global unknown
    global revision
    global build_date
    global serial_number
    global partnumber
    print('MAJOR BOARD TYPE')
    if p_number == 'P22276' or 'R22276':
        if board_type == '156':
            major_board_type = 'M40'
            if config_cal == '102':
                board_voltage = 'HIGH'

#******************************************************************************************
def ScanBarcode(port):
    global major_board_type
    global board_voltage
    global p_number
    global board_type
    global config_cal
    global unknown
    global revision
    global build_date
    global serial_number
    global partnumber
    try:
        print('Looking for barcode scanner...')  # check which port was really used
        with serial.Serial(port, 115200, timeout=1) as ser:
            print('Found barcode scanner on port ' + ser.name)
            ser.write(b'\x16T\r')   #write trigger
            print('Sending trigger  \x16T\r')
            #TODO: make sure this isnt blocking and contains enough characters read
            line = ser.read(30)     #check for return data
            ser.write(b'\x16U\r')   #send off trigger
            line = line.decode('ascii')
            print(line)
    except OSError as err:
        print(err)
        return False, err

    try:
        if not line:
            print('Failed to scan')
            return False,('Failed to scan')
        else:
            print('Data returned from scanner')
            nodashes = str(line).split('-')
            print(nodashes)
            spaces = nodashes[3]
            nospaces = spaces.split()
            print(nospaces)
            p_number = nodashes[0]
            board_type = nodashes[1]
            config_cal = nodashes[2]
            unknown =  nospaces[0]
            revision = nospaces[1]
            build_date =  nospaces[2]
            serial_number =  nospaces[3]
            partnumber = p_number + '-' + board_type + '-' + config_cal + '-' + unknown + '-' + revision + '-' + build_date + '-' + serial_number
            filename = partnumber + '.txt'
            MajorBoardType(p_number, board_type, config_cal)
            print('Filename ' + filename)
            cf.config_write('UUT', 'PART_NUMBER', partnumber)
            cf.config_write('UUT', 'P_NUMBER', p_number)
            cf.config_write('UUT', 'BOARD', board_type)
            cf.config_write('UUT', 'CONFIG_CAL', config_cal)
            cf.config_write('UUT', 'UNKNOWN', unknown)
            cf.config_write('UUT', 'REVISION', revision)
            cf.config_write('UUT', 'BUILD_DATE', build_date)
            cf.config_write('UUT', 'SERIAL_NUMBER', serial_number)
            cf.config_write('UUT', 'MAJOR_BOARD_TYPE', major_board_type)
            cf.config_write('UUT', 'BOARD_VOLTAGE', board_voltage)

            lf.config_write(filename, 'BOARD', 'part_number', filename)
            lf.config_write(filename, 'BOARD', 'p_number', p_number)
            lf.config_write(filename, 'BOARD', 'board type', board_type)
            lf.config_write(filename, 'BOARD', 'config calibration',config_cal)
            lf.config_write(filename, 'BOARD', 'unknown', unknown)
            lf.config_write(filename, 'BOARD', 'revision', revision)
            lf.config_write(filename, 'BOARD', 'build data' , build_date)
            lf.config_write(filename, 'BOARD', 'serial_number', serial_number)
            lf.config_write(filename, 'BOARD', 'board_major_type', board_major_type)
            lf.config_write(filename, 'BOARD', 'k60_firmware_version', cf.config_read('M40_FIRMWARE', 'm40_k60_firmware_version'))
            lf.config_write(filename, 'BOARD', 'web_page_version', cf.config_read('M40_FIRMWARE', 'm40_web_page_firmware_version'))
            lf.config_write(filename, 'BOARD', 'meter_ic_version', cf.config_read('M40_FIRMWARE', 'm40_meter_ic_firMware_version'))
            lf.config_write(filename, 'BOARD', 'wifi_firmware_version', cf.config_read('M40_FIRMWARE', 'm40_meter_ic_firmware_version'))
            lf.config_write(filename, 'TEST_DATE_TIME', 'test_time' , time.strftime('%H:%M:%S'))
            lf.config_write(filename, 'TEST_DATE_TIME', 'test_date' , time.strftime('%d:%m:%Y'))
            #
            print('UUT', 'PART_NUMBER', partnumber)
            print('UUT', 'P_NUMBER', p_number)
            print('UUT', 'BOARD', board_type)
            print('UUT', 'CONFIG_CAL', config_cal)
            print('UUT', 'UNKNOWN', unknown)
            print('UUT', 'REVISION', revision)
            print('UUT', 'BUILD_DATE', build_date)
            print('UUT', 'SERIAL_NUMBER', serial_number)
            print('UUT', 'MAJOR_BOARD_TYPE', major_board_type)
            print('UUT', 'BOARD_VOLTAGE', board_voltage)
            print('BOARD', 'part_number', filename)
            print('BOARD', 'p_number', p_number)
            print('BOARD', 'board type', board_type)
            print('BOARD', 'config calibration', config_cal)
            print('BOARD', 'unknown', unknown)
            print('BOARD', 'revision', revision)
            print('BOARD', 'build data', build_date)
            print('BOARD', 'serial_number', serial_number)
            print('BOARD', 'k60_firmware_version',
                            cf.config_read('M40_FIRMWARE', 'm40_k60_firmware_version'))
            print('BOARD', 'web_page_version',
                            cf.config_read('M40_FIRMWARE', 'm40_web_page_firmware_version'))
            print('BOARD', 'meter_ic_version',
                            cf.config_read('M40_FIRMWARE', 'm40_meter_ic_firMware_version'))
            print('BOARD', 'wifi_firmware_version',
                            cf.config_read('M40_FIRMWARE', 'm40_meter_ic_firmware_version'))
            print('TEST_DATE_TIME', 'test_time', time.strftime('%H:%M:%S'))
            print('TEST_DATE_TIME', 'test_date', time.strftime('%d:%m:%Y'))
            return True, str(line)
        ser.close()  # close port
    except OSError as err:
        print(err)
        return False, err

#******************************************************************************************
def mbComm(comport, address, register):

    try:
        uut = minimalmodbus.Instrument(comport, address)
        uut.debug = False
        uut.serial.timeout = 2.0
        uut.serial.bytesize = 8
        uut.serial.parity  = minimalmodbus.serial.PARITY_NONE
        uut.serial.baudrate = 19200
        uut.serial.stopbits = 1
        uut.mode = minimalmodbus.MODE_RTU
        uut.close_port_after_each_call = False
        count = 0
        while count < 5:
            #value = uut.read_register(register, 1, 4)     #register, number of decimals
            value = uut.read_float(register)  # register, number of decimals
            print('Value->' + str(value))
            time.sleep(0.100)
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

#******************************************************************************************
def __init__(self):
    super().__init__()
    self.initUI()

#******************************************************************************************
def main():

    module = 'A'

    host_address = 1
    comport = 'COM44'
    #comport = '/dev/tty.usbserial-FT084UEL'
    register = 490

    if module == "A":
        ret = mbComm(comport, host_address, register)

    if module == "B":
        global port
        port = 'COM4'
        # port ='/dev/tty.usbmodem14444331'
        ret = ScanBarcode(port)

    if module == "C":
        ret = collectSerialPorts()


    print(ret)

#******************************************************************************************
if __name__ == '__main__':
    main()
