#this module will scan a barcode
#i may parse the data here or may
#do a built in regex.

import time
import serial
import Configuration as cf
import Logfile as lf

def ScanBarcode(port):
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
            print('Filename ' + filename)
            cf.config_write('UUT', 'PART_NUMBER', partnumber)
            cf.config_write('UUT', 'P_NUMBER', p_number)
            cf.config_write('UUT', 'BOARD', board_type)
            cf.config_write('UUT', 'CONFIG_CAL', config_cal)
            cf.config_write('UUT', 'UNKNOWN', unknown)
            cf.config_write('UUT', 'REVISION', revision)
            cf.config_write('UUT', 'BUILD_DATE', build_date)
            cf.config_write('UUT', 'SERIAL_NUMBER', serial_number)
            lf.config_write(filename, 'BOARD', 'part_number', filename)
            lf.config_write(filename, 'BOARD', 'p_number', p_number)
            lf.config_write(filename, 'BOARD', 'board type', board_type)
            lf.config_write(filename, 'BOARD', 'config calibration',config_cal)
            lf.config_write(filename, 'BOARD', 'unknown', unknown)
            lf.config_write(filename, 'BOARD', 'revision', revision)
            lf.config_write(filename, 'BOARD', 'build data' , build_date)
            lf.config_write(filename, 'BOARD', 'serial_number', serial_number)
            lf.config_write(filename, 'BOARD', 'k60_firmware_version', cf.config_read('M40_FIRMWARE', 'm40_k60_firmware_version'))
            lf.config_write(filename, 'BOARD', 'web_page_version', cf.config_read('M40_FIRMWARE', 'm40_web_page_firmware_version'))
            lf.config_write(filename, 'BOARD', 'meter_ic_version', cf.config_read('M40_FIRMWARE', 'm40_meter_ic_firMware_version'))
            lf.config_write(filename, 'BOARD', 'wifi_firmware_version', cf.config_read('M40_FIRMWARE', 'm40_meter_ic_firmware_version'))
            lf.config_write(filename, 'TEST_DATE_TIME', 'test_date' , time.strftime('%H:%M:%S'))
            lf.config_write(filename, 'TEST_DATE_TIME', 'test_time' , time.strftime('%d:%m:%Y'))
            return True, str(line)
        ser.close()  # close port
    except OSError as err:
        print(err)
        return False, err


def __init__(self):
    super().__init__()
    self.initUI()


def main():
    global port
    port = 'COM4'
    #port ='/dev/tty.usbmodem14444331'
    ScanBarcode(port)
    pass


if __name__ == '__main__':
    main()
