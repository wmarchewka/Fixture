#native libraries
import base64
import configparser
import os
import socket
import telnetlib
import threading
import time

global osname
osname = sl.getOsPlatform()
#other libraries
try:
    import RPi.GPIO as gp
except ImportError:
    import FakeRPi.GPIO as gp
from PyQt5.QtWidgets import *

#my libraries
from QT_Project import mainwindow_auto as mw
from PyQt5.QtCore import pyqtSignal
from OLD_Files import EthernetCommLibrary as el, FileConfigurationLibrary as fl, SerialBarCodeModbusLibrary as ml, \
    ProgrammersLibrary as pl
import OLD_Files.SupportLibrary as sl
import sys
try:
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO
global demojm_serial_port
global Testing
import minimalmodbus
import serial
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

class MainWindow(QMainWindow, mw.Ui_MainWindow):

    global DemoJM_Serialport
    serialtrigger = pyqtSignal(bytes)

    def __init__(self):
        os_name = sl.getOsPlatform()
        print('os name->' + os_name)
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file
        self.serialtrigger.connect(self.parse_serial_data)
        serial_ports_list = ml.collectSerialPorts()                                            #run serial port routine
        self.cbTFP3ComPort.addItems(serial_ports_list)
        self.cbScannerComPort.addItems(serial_ports_list)
        self.cbCycloneComPort.addItems(serial_ports_list)
        self.cbModbusComPort.addItems(serial_ports_list)
        self.cbDemoJMComPort.addItems(serial_ports_list)
        self.pbPowerOn.clicked.connect(lambda: self.power_up_relay())
        self.pbPowerOff.clicked.connect(lambda: self.power_down_relay())
        self.pbSendTelnet.clicked.connect(lambda: self.pressedTelnetButton())
        self.pbTelnetGetVoltages.clicked.connect(lambda: self.GetVoltages())
        self.pbReadScanner.clicked.connect(lambda: self.pressedSendScannerButton())
        self.pbDoPing.clicked.connect(lambda: self.PingUUT())
        self.pbProgCyclone.clicked.connect(lambda: self.programCyclone())
        self.pbProgTFP3.clicked.connect(lambda: self.pressedTFP3Button())
        self.cbTFP3ComPort.currentIndexChanged.connect(self.tfp3SerialPortChanged)
        self.cbScannerComPort.currentIndexChanged.connect(self.ScannerSerialPortChanged)
        self.cbCycloneComPort.currentIndexChanged.connect(self.CycloneSerialPortChanged)
        self.cbModbusComPort.currentIndexChanged.connect(self.ModbusSerialPortChanged)
        self.cbDemoJMComPort.currentIndexChanged.connect(self.DemoJMSerialPortChanged)
        self.cbDemoJMComPort.activated[str].connect(self.DemoJMSerialPortChanged)
        self.lnSerialTest.textChanged.connect(self.SerialTest)
        self.check_for_config()                                                                 #open configuration file
        self.populate_defaults()
        print('TFP3 relay pin ' + str(sl.gpio_tfp3relay_pin))
        self.check_serial_event()

    gpio_powerrelay = 7
    gpio_tfp3relay_pin = 3
    cyclone_recv1 = b'jP&E,14,Universal_PEMBC0F62,none,0,0,Dec 12 2016,9.80,Rev. A,00:0d:01:bc:0f:62,0,1,K70FN1M0_EMMC,ArmCortex,'
    cyclone_recv2 = b'hP&E,14,Universal_PEMBC0F62,none,0,0,Dec 12 2016,9.80,Rev. A,00:0d:01:bc:0f:62,0,1,K70FN1M0_EMMC,Generic,'

    # ******************************************************************************************
    def CycloneProgram(port):
        # open com port wait for error
        try:
            print('Looking for scanner...')
            ser = serial.Serial(port, 115200, timeout=1)
        except:
            print('Cyclone error...')
            return False, "Com Error"
        # port found send commands to identify what it is
        ser.write(b'\x03\x01\x18\x5d')  # first command
        print('SEND->\\x03\\x01\\x18\\x5d')  #
        line = ser.read(2)  # response should be 01 00
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
                ser.write(b'\x03\x18\x5f\x65')  # this is the command to start programming
                time.sleep(0.5)
                print('SEND->\\x03\\x18\\x5f\\x65')
                line = ser.readline()
                print('RECV->' + str(line))
                if line == b'\x03\x01\x01\xee':  # responce will be 03 00 00 ee until we recv a 03 01 01 ee
                    ser.write(b'\x03\x18\x33\x66')  # send to get status
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
            se = serial.Serial(port, 115200)
            se.write(b'P\r\n')
            print('Writing P to programmer')
            x = se.read_until(terminator=b'Programming')
            print(x)
            if x != b'P\r\r\nProgramming':
                print('Did not find TFP3 programmer')
                return False, 'TFP3 programmer not found'
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
                            return False, 'TFP3 timeout programming'
                        elif data.find(b'successful') > -1:
                            print('Success')
                            return True, 'TFP3 program success'
        except:
            return False, 'Serial port error'
            print('Serial port error')

    # ******************************************************************************************
    def gpioInit():
        # global powerrelay_pin
        # global tfp3relay_pin
        # example
        # GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  PUD_UP
        # GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
        # add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
        # GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_tfp3relay_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(gpio_tfp3relay_pin, GPIO.OUT, initial=GPIO.LOW)
        gpio_on = 1
        gpio_off = 0

    # ******************************************************************************************
    def getOsPlatform():
        platforms = {
            'linux1': 'Linux',
            'linux2': 'Linux',
            'darwin': 'OSX',
            'win32': 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        return platforms[sys.platform]

    # ******************************************************************************************
    def testlogConfigWrite(section, key, value):

        config = configparser.RawConfigParser()
        config.read('configuration.cfg')

        try:
            config.add_section(section)
            config.set(section, key, value)
            with open('configuration.cfg', 'w') as configfile:
                config.write(configfile)
        except:
            config.set(section, key, value)
            with open('configuration.cfg', 'w') as configfile:
                config.write(configfile)

    # ******************************************************************************************
    def testlogConfigRead(section, key):

        config = configparser.RawConfigParser()
        config.read('configuration.cfg')

        try:
            value = config.get(section, key)
            return value
        except:
            return ('ERROR')

    # ******************************************************************************************
    def logfileWriteDefaults():

        try:
            config = configparser.RawConfigParser()
            config.read('master_logfile.cfg')
            print(config)

            config.add_section('BOARD')
            config.set('BOARD', 'part_number', '')
            config.set('BOARD', 'p_number', '')
            config.set('BOARD', 'board_type', '')
            config.set('BOARD', 'config_calibration', '')
            config.set('BOARD', 'unknown', '')
            config.set('BOARD', 'revision', '')
            config.set('BOARD', 'serial_ number', '')
            config.set('BOARD', 'board_major_type', '')
            config.set('BOARD', 'build_date', '')
            config.set('BOARD', 'mac_address', '')
            config.set('BOARD', 'k60_firmware_version', '')
            config.set('BOARD', 'web_page_firmware_version', '')
            config.set('BOARD', 'meter_ic_firmware_version', '')
            config.set('BOARD', 'wifi_firmware_version', '')
            config.add_section('TEST_DATE_TIME')
            config.set('TEST_DATE_TIME', 'test_date', '')
            config.set('TEST_DATE_TIME', 'test_time', '')
            config.add_section('TEST_RESULTS')
            config.set('TEST_RESULTS', 'Programming', '')
            config.set('TEST_RESULTS', 'Reset_Button', '')
            config.set('TEST_RESULTS', 'Status_LEDs', '')
            config.set('TEST_RESULTS', 'Ethernet_Port_1_LEDs', '')
            config.set('TEST_RESULTS', 'Ethernet_Port_2_LEDs', '')
            config.set('TEST_RESULTS', 'Ethernet_Port_1_Read', '')
            config.set('TEST_RESULTS', 'Ethernet_Port_2_Read', '')
            config.set('TEST_RESULTS', 'Ethernet_Write', '')
            config.set('TEST_RESULTS', 'Modbus_Port_1_Read', '')
            config.set('TEST_RESULTS', 'Modbus_Port_2_Read', '')
            config.set('TEST_RESULTS', 'Modbus_Write', '')
            config.set('TEST_RESULTS', 'Flash_Memory', '')
            config.set('TEST_RESULTS', 'ADC_Read', '')
            config.set('TEST_RESULTS', 'Data_Request', '')
            config.set('TEST_RESULTS', 'MAC_Address_Test', '')

            with open('master_logfile.cfg', 'w') as configfile:
                config.write(configfile)
            with open('logfile.cfg', 'w') as configfile:
                config.write(configfile)

        except:

            return ValueError

    # ******************************************************************************************
    def configfileWriteDefaults():

        try:
            config = configparser.RawConfigParser()
            config.read('master_configuration.cfg')
            print(config)

            config.add_section('CONFIG')
            config.set('CONFIG', 'FILE_VER', '1')
            config.add_section('DEMOJM')
            config.set('DEMOJM', 'COM_PORT', 'COM1')
            config.add_section('SCANNER')
            config.set('SCANNER', 'COM_PORT', 'COM1')
            config.add_section('CYCLONE')
            config.set('CYCLONE', 'COM_PORT', 'COM1')
            config.add_section('TFP3')
            config.set('TFP3', 'COM_PORT', 'COM1')
            config.add_section('MODBUS')
            config.set('MODBUS', 'COM_PORT', 'COM1')
            config.set('MODBUS', 'BAUD_RATE', '19200')
            config.set('MODBUS', 'DATA_BITS', '8')
            config.set('MODBUS', 'PARITY', 'NONE')
            config.set('MODBUS', 'STOP_BITS', '1')
            config.set('MODBUS', 'FLOW_CONTROL', 'NONE')
            config.set('MODBUS', 'TIME_OUT', '2000')
            config.set('MODBUS', 'MODE', 'RTU')
            config.set('MODBUS', 'SLAVE_ADDRESS', '1')
            config.add_section('TELNET')
            config.set('TELNET', 'IP_ADDRESS', '192.168.1.99')
            config.add_section('MAC_ADDRESS')
            config.set('MAC_ADDRESS', 'NEXT_MAC', '58:2F:42:80:00:B3')
            config.set('MAC_ADDRESS', 'MIN_MAC', '58:2F:42:80:00:00')
            config.set('MAC_ADDRESS', 'MAX_MAC', '58:2F:42:8F:FF:FF')
            config.add_section('M40_FOLDERS')
            config.set('M40_FOLDERS', 'BASE', "C:\\UEC\\Functional Test\\M40")
            config.set('M40_FOLDERS', 'TEST_REPORTS', 'C:\\UEC\\Functional Test\\M40\\Test Reports\\Dual Ethernet')
            config.set('M40_FOLDERS', 'CONFIGURATION', 'C:\\UEC\\Functional Test\\M40\\Configuration')
            config.set('M40_FOLDERS', 'M40_FIRMWARE',
                       'C:\\UEC\\Functional Test\\M40\\Configuration\\firmware_v3.39.bin')
            config.set('M40_FOLDERS', 'M40_WIFI_FIRMWARE',
                       'C:\\UEC\\Functional Test\\M40\\Configuration\\wifi_v0x2124a503.bin')
            config.set('M40_FOLDERS', 'M40_WEB_PAGE_UPLOAD',
                       'C:\\UEC\\Functional Test\\M40\\Configuration\\web_pages_UEC025_ENG.tfs')
            config.set('M40_FOLDERS', 'M40_METER_IC_FIRMWARE',
                       'C:\\UEC\\Functional Test\\M40\\Configuration\\meter_v1.20.hex')
            config.add_section('M50_FOLDERS')
            config.set('M50_FOLDERS', 'M50_BASE', 'C:\\UEC\\Functional Test\\M50')
            config.set('M50_FOLDERS', 'M50_TEST_REPORTS', 'C:\\UEC\\Functional Test\\M50\\Test Reports\\')
            config.set('M50_FOLDERS', 'M50_CONFIGURATION', 'C:\\UEC\\Functional Test\\M50\\Configuration\\')
            config.set('M50_FOLDERS', 'M50_MASTER_TEST_REPORT',
                       'C:\\UEC\\Functional Test\\M50\\Test Reports\\Dual Ethernet\\')
            config.set('M50_FOLDERS', 'M50_MASTER_TEST_REPORT',
                       'C:\\UEC\\Functional Test\\M50\\Test Reports\\Dual Ethernet\\')
            config.add_section('M40_FIRMWARE')
            config.set('M40_FIRMWARE', 'M40_K60_FIRMWARE_VERSION', 'firmware_v3.39.bin')
            config.set('M40_FIRMWARE', 'M40_WIFI_FIRMWARE_VERSION', 'wifi_v0x2124a503.bin')
            config.set('M40_FIRMWARE', 'M40_WEB_PAGE_FIRMWARE_VERSION', 'web_pages_UEC025_ENG.tfs')
            config.set('M40_FIRMWARE', 'M40_METER_IC_FIRMWARE_VERSION', 'meter_v1.20.hex')
            config.add_section('M50_FIRMWARE')
            config.set('M50_FIRMWARE', 'M50_K60_FIRMWARE_VERSION', 'firmware_v3.39.bin')
            config.set('M50_FIRMWARE', 'M50_WIFI_FIRMWARE', 'wifi_v0x2124a503.bin')
            config.set('M50_FIRMWARE', 'M50_WEB_PAGE_FIRMWARE_VERSION', 'web_pages_UEC025_ENG.tfs')
            config.set('M50_FIRMWARE', 'M50_METER_IC_FIRMWARE_VERSION', 'meter_v1.20.hex')
            config.add_section('UUT')
            config.set('UUT', 'IP_ADDRESS', '192.168.1.99')
            config.set('UUT', 'P_NUMBER', '')
            config.set('UUT', 'PART_NUMBER', '')
            config.set('UUT', 'BOARD', '')
            config.set('UUT', 'CONFIG_CAL', '')
            config.set('UUT', 'DONT_KNOW', '')
            config.set('UUT', 'REVISION', '')
            config.set('UUT', 'BUILD_DATE', '')
            config.set('UUT', 'SERIAL_NUMBER', '')
            config.set('UUT', 'MAJOR_BOARD_TYPE', '')
            config.set('UUT', 'BOARD_VOLTAGE', '')

            with open('master_configuration.cfg', 'w') as configfile:
                config.write(configfile)
            with open('configuration.cfg', 'w') as configfile:
                config.write(configfile)
        except:
            return ValueError

    # ******************************************************************************************
    def logfileWrite(filename, section, key, value):

        config = configparser.RawConfigParser()
        config.read(filename)

        try:
            config.add_section(section)
            config.set(section, key, value)
            with open(filename, 'w') as configfile:
                config.write(configfile)
        except:
            config.set(section, key, value)
            with open(filename, 'w') as configfile:
                config.write(configfile)

    # ******************************************************************************************
    def logfileRead(filename, section, key):

        config = configparser.RawConfigParser()
        config.read(filename)

        try:
            value = config.get(section, key)
            return value
        except:
            return ('ERROR')

    # ******************************************************************************************
    def configfileWrite(section, key, value):

        config = configparser.RawConfigParser()
        config.read('configuration.cfg')
        print('Writing to config->Section:' + section + 'Key:' + key + ' Value: ' + value)
        try:
            config.add_section(section)
            config.set(section, key, value)
            with open('configuration.cfg', 'w') as configfile:
                config.write(configfile)
        except:
            config.set(section, key, value)
            with open('configuration.cfg', 'w') as configfile:
                config.write(configfile)

    # ******************************************************************************************
    def configfileRead(section, key):
        config = configparser.RawConfigParser()
        config.read('configuration.cfg')
        try:
            value = config.get(section, key)
            print('Reading from config-> Section:' + section + ' Key:' + key + ' Value: ' + value)
            return value
        except:
            return ('ERROR')

    # ******************************************************************************************



    # ******************************************************************************************
    def pinguut(ip_add, secs):
        pingcount = 0
        while True:
            print("pinging UUT at ip " + ip_add + ' count ' + str(pingcount))
            if sl.getOsPlatform() == 'Linux':
                data = ('ping ' + ip_add + ' -w 1000 -c 1')  # set ping timeout to 1000ms
            elif sl.getOsPlatform() == 'Windows':
                data = ('ping ' + ip_add + ' -w 1000 -n 1')
            elif sl.getOsPlatform() == 'OSX':
                data = ('ping ' + ip_add + ' -W 1000 -c 1')
            response = os.system(data)  # default ping takes 3 secs to respond
            print(response)
            if response == 0:
                print(ip_add + ' is up!')
                return True, ip_add + ' is up!'
            else:
                print(ip_add + ' is down!')
                pingcount = pingcount + 1
                if pingcount > secs:
                    return False, ip_add + ' is down!'

    # ******************************************************************************************
    def check_reset_button(ip_add):
        global respond_initial
        global reset
        while True:
            val = pinguut(ip_add)
            if val:
                respond_initial = True
            print('press reset button')
            time.sleep(2)
        if not respond_initial:
            print('did not respond to initial ping')
            return False, 'Did not respond to initial ping'
        if respond_initial == True and val == False:
            print('Unit resetting...')
            reset = True
        if val == True and reset == True:
            print("Successfully reset...")
            return True, "Successfully reset..."


# ******************************************************************************************
def write_lan_mac(ip_add):
    try:
        host = ip_add
        port = 23
        print('Starting button test on ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(2)
        conn = host, port
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$lanmac,G\r\n')
        old_mac = sc.recv(100)
        old_mac = old_mac.decode().split(',')[2]
        print('old_mac -> ' + old_mac)
        old_mac = str(old_mac)
        new_mac = old_mac
        print('new_mac -> ' + new_mac)
        se = '$lanmac,S,' + new_mac + str('\r\n')
        sc.send(se.encode())
        data = sc.recv(100)
        print('data->' + str(data))
        result = data.decode().split(',')[3].find('OK')
        print('result->' + str(result))
        if result > 0:
            print('Lan Mac not set')
            return False, "Lan Mac not set"
        else:
            print('Lan Mac successfully set')
            return True, 'Lan Mac successfully set'

    except OSError as err:
        print(err)
        return False, err


# ******************************************************************************************
def getvoltages(ip_add):
    try:
        HOST = ip_add
        print("Getting Voltages from " + HOST)
        PORT = 23
        TIMEOUT = 5
        tn = telnetlib.Telnet(host=HOST, port=PORT, timeout=TIMEOUT)
        tn.set_debuglevel(0)
        tn.write(b"$login,factory,factory\n")
        tn.write(b"$mdra,0,U0512,U377520\n")
        tn.write(b"$mdra,0,U0513,U377520\n")
        tn.write(b"$mdra,0,U0514,U377520\n")
        tn.write(b"$mdra,0,215,000000C0\n")
        tn.write(b"$mdra,0,U0007\n")
        tn.write(b"$mdra,0,U0008\n")
        tn.write(b"$mdra,0,U0009\n")
        # TODO need to scale these values upon return
        tn.write(b"$mdra,0,U0518,U5000\n")
        tn.write(b"$mdra,0,U0519,U5000\n")
        tn.write(b"$mdra,0,U0520,U5000\n")
        tn.write(b"$mdra,0,U0521,U5000\n")
        tn.write(b"$mdra,0,U0522,U5000\n")
        tn.write(b"$mdra,0,U0523,U5000\n")
        tn.write(b"$mdra,0,215,000000C0\n")
        # TODO need burden resistor value from config
        tn.write(b"$mdra,0,U0018\n")
        tn.write(b"$mdra,0,U0026\n")
        tn.write(b"$mdra,0,U0034\n")
        tn.write(b"$mdra,0,U0042\n")
        tn.write(b"$mdra,0,U0050\n")
        tn.write(b"$mdra,0,U0058\n")
        tn.write(b"\r")
        tempdata = tn.read_all().decode('ascii')
        tn.close()
        tempdata = tempdata.split(',')
        voltageA = float(tempdata[tempdata.index('U0007') + 1]) / 1000
        voltageB = float(tempdata[tempdata.index('U0008') + 1]) / 1000
        voltageC = float(tempdata[tempdata.index('U0009') + 1]) / 1000
        currentA = float(tempdata[tempdata.index('U0018') + 1]) / 1000
        currentAneg = float(tempdata[tempdata.index('U0026') + 1]) / 1000
        currentB = float(tempdata[tempdata.index('U0034') + 1]) / 1000
        currentBneg = float(tempdata[tempdata.index('U0042') + 1]) / 1000
        currentC = float(tempdata[tempdata.index('U0050') + 1]) / 1000
        currentCneg = float(tempdata[tempdata.index('U0058') + 1]) / 1000
        print(voltageA, voltageB, voltageC)
        print(currentA, currentAneg, currentB, currentBneg, currentC, currentCneg)
        return True, tempdata


    except OSError as err:
        # tn.close
        print(err)
        return False, err


# ******************************************************************************************
def m40buttontest():
    try:
        host = "192.168.1.8"
        port = 23
        # HOST = '10.0.0.210'
        print('Starting button test on ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = host, port
        PORT = 23
        TIMEOUT = 5
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        # tn = telnetlib.Telnet(host=HOST, port=PORT, timeout=TIMEOUT)
        # tn.write(b'$login,factory,factory\n')
        # tn.write(b"$bts,s,0\n")
        # tn.write(b"$bts,G\n\r")
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$bts,s,0\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$bts,G\r\n')
        data = sc.recv(100)
        print(data)
        t = 0
        p = ''
        while True:
            sc.send(b'$bts,G\r\n')
            data = sc.recv(100)
            print(data)
            time.sleep(1)
            t = t + 1
            print('t ' + str(t))
            if t == 25:
                break
            d = str(data).split(',')
            d = d[2]
            if p != d:
                t = 0
            p = d
            print(d.encode('ascii'))
            if d == '1':
                print('press button 1')
                r = 1
            if d == '2':
                print('press button 2')
            if d == '3':
                print('press button 3')
            if d == '4':
                print('press button 4')
            if d == '5':
                print('Unit passed button test')
                sc.close
                return True, "Unit passed Button Test"
        print("timeout")
        sc.close()
        False, "Timeout"


    except OSError as err:
        print(err)
        return False, err


# ******************************************************************************************
def modbusinit(ip_add):
    print("Setting modbus defaults")
    PORT = 23
    TIMEOUT = 5
    tn = telnetlib.Telnet(host=ip_add, port=PORT, timeout=TIMEOUT)
    tn.write(b'$login,factory,factory\n')
    tn.write(b'$modbd,s,19200\n')
    tn.write(b'$modp,s,1\n')
    tn.write(b'$modst,s,1\n')
    tn.write(b'$reboot\n')
    tn.write(b'\r')
    tempdata = tn.read_all().decode('ascii')
    print(tempdata)
    tn.close()

    return tempdata


# ******************************************************************************************
def setpcr(host):
    try:
        print("Setting PCR value on " + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 23
        conn = host, port
        sc.settimeout(2)
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$PCR,S,E0100110\r\n')
        data = sc.recv(100)
        print('data -> ' + str(data))
        data = data.decode().split(',')[3].find('OK')
        sc.close()
        if data > 0:
            print('PCR not set')
            return False, "PCR not set"
        else:
            print('PCR successfully set')
            return True, 'PCR successfully set'

    except socket.timeout as err:
        print('socket timeout')
        return False, err

    except socket.error as err:
        print('socket error')
        return False, err

    except OSError as err:
        sc.close
        print(err)
        return False, err


# ******************************************************************************************
def write_serialnumber(host):
    try:
        port = 23
        print('Starting button test on ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(2)
        conn = host, port
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$wlanmac,G\r\n')
        old_mac = sc.recv(100)
        old_mac = old_mac.decode().split(',')[2]
        print('old_mac -> ' + old_mac)
        old_mac = str(old_mac)
        new_mac = old_mac
        print('new_mac -> ' + new_mac)
        se = '$wlanmac,S,' + new_mac + str('\r\n')
        sc.send(se.encode())
        data = sc.recv(100)
        print('data->' + str(data))
        result = data.decode().split(',')[3].find('OK')
        print('result->' + str(result))
        if result > 0:
            print('Wireless lan mac not set')
            return False, "Wireless lan mac not set"
        else:
            print('Wireless lan mac successfully set')
            return True, 'Wireless lan mac successfully set'

    except OSError as err:
        print(err)
        return False, err


# ******************************************************************************************
def write_wifi_mac(host):
    try:
        port = 23
        print('Setting wireless LAN MAC ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(2)
        conn = host, port
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$wlanmac,G\r\n')
        old_mac = sc.recv(100)
        old_mac = old_mac.decode().split(',')[2]
        print('old_mac -> ' + old_mac)
        old_mac = str(old_mac)
        new_mac = old_mac
        print('new_mac -> ' + new_mac)
        se = '$wlanmac,S,' + new_mac + str('\r\n')
        sc.send(se.encode())
        data = sc.recv(100)
        print('data->' + str(data))
        result = data.decode().split(',')[3].find('OK')
        print('result->' + str(result))
        if result > 0:
            print('Wireless lan mac not set')
            return False, "Wireless lan mac not set"
        else:
            print('Wireless lan mac successfully set')
            return True, 'Wireless lan mac successfully set'

    except OSError as err:
        print(err)
        return False, err


# ******************************************************************************************
def file_size(fname):
    import os
    statinfo = os.stat(fname)
    return statinfo.st_size


# ******************************************************************************************
def upload_file(slot):
    try:
        boardtype = fl.configfileRead('UUT', "major_board_type")
        if boardtype == "M40":
            section = 'M40_FOLDERS'
        if boardtype == "M50":
            section = 'M50_FOLDERS'
        if boardtype == "M60":
            section = 'M60_FOLDERS'

        if slot == 'wifi':
            key = 'm40_wifi_firmware'
        if slot == 'web':
            key = 'm40_web_page_upload'
        if slot == 'meter':
            key = 'm40_meter_ic_firmware'
        if slot == 'firmware':
            key = 'm40_firmware'

        path = fl.configfileRead(section, key)
        host = fl.configfileRead('TELNET', "ip_address")
        user = 'factory'
        password = 'factory'
        port = 80
        print('Starting uploading of file ' + path + ' to  ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(5)
        conn = host, port
        sc.connect(conn)

        fsize = file_size(path)
        filename = open(path, "br")
        fn = filename.read()

        myauthorization = base64.b64encode(user.encode('ascii') + b":" + password.encode('ascii'))

        my_req_body = "-----------------------------7dd3201c5104d4\r\n"
        my_req_body = my_req_body + 'Content-Disposition: form-data; name="' + str(slot) + '"; filename="' + str(
            path) + '"\r\n'
        my_req_body = my_req_body + 'Content-Type: application/octet-stream'
        my_req_body = my_req_body + '\r\n\r\n'
        my_req_end = "\r\n-----------------------------7dd3201c5104d4\r\n"

        print('Length of body->' + str(len(my_req_body)))
        print('Length of file->' + str(fsize))
        print('Length of end->' + str(len(my_req_end)))

        totalsize = len(my_req_body) + fsize + len(my_req_end)
        print('Total size->' + str(totalsize))

        my_req_head = "POST /upload_file.cgi HTTP/1.1\r\n"
        my_req_head = my_req_head + "Accept-Language: en-us\r\n"
        my_req_head = my_req_head + "Host: " + str(host) + "\r\n"
        my_req_head = my_req_head + "Content-Type: multipart/form-data; boundary=---------------------------7dd3201c5104d4\r\n"
        my_req_head = my_req_head + "Content-Length: " + str(totalsize) + "\r\n"
        my_req_head = my_req_head + "Connection: Keep-Alive\r\n"
        my_req_head = my_req_head + "Authorization: Basic " + str(myauthorization, 'utf-8')  # ZmFjdG9yeTpmYWN0b3J5"
        my_req_head = my_req_head + "\r\n\r\n"
        my_req_head = my_req_head + "\r\n"

        # sys.stdout.write(my_req_head)
        # sys.stdout.write(my_req_body)
        # sys.stdout.buffer.write(fn)
        # sys.stdout.write(str(my_req_end))

        buffer = my_req_head.encode('ascii') + my_req_body.encode('ascii')
        while buffer:
            bytes = sc.send(buffer)
            buffer = buffer[bytes:]
        data = sc.recv(250)
        print('return data-------------------------')
        print(data)

        buffer = fn
        while buffer:
            bytes = sc.send(buffer)
            buffer = buffer[bytes:]
        data = sc.recv(1000)
        print('return data-------------------------')
        print(data)

        buffer = my_req_end.encode('ascii')
        while buffer:
            bytes = sc.send(buffer)
            buffer = buffer[bytes:]
        data = sc.recv(500)
        print('return data-------------------------')
        # data = str(data)
        print(data)
        data = sc.recv(500)
        print('return data-------------------------')
        print(data)
        data = str(data)
        sc.close()
        if data.find('url=upload.html'):
            print('upload sucessful')
        else:
            print('upload failed')

    except OSError as err:
        print(err)
        return False, err


# ******************************************************************************************
def write_script(host, path):
    try:
        port = 23
        print('Uploading script ' + path)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(5)
        conn = host, port
        script = open(path, 'br')
        fn = script.read()
        print('file-> ' + str(fn))
        sc.connect(conn)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print('login data>' + str(data))
        splitdata = fn.split(b'\r\n')
        print(splitdata)
        for linedata in splitdata:
            sc.send(linedata + b'\r\n')
            data = sc.recv(1000)
            print('data->' + str(data))


    except OSError as err:
        print(err)
        return False, err


# ******************************************************************************************
def check_webpageversion(host):
    try:
        port = 23
        print('Checking webpage version...')
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(5)
        conn = host, port
        sc.connect(conn)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print('login data-' + str(data))
        sc.send('')
        data = sc.recv(100)
        print('return data->' + str(data))



    except OSError as err:
        print(err)
        return False, err


# ******************************************************************************************
def setup_wifi(host, new_mac):
    try:
        port = 23
        print('Starting WIFI Configuration ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(2)
        conn = host, port
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$wlanmac,G\r\n')
        old_mac = sc.recv(100)
        old_mac = old_mac.decode().split(',')[2]
        old_mac = str(old_mac)
        if old_mac == 'N/A':
            print('No WIFI MAC Found')
            return False, "No WIFI MAC found"
        else:
            print("Current MAC " + old_mac)
        if new_mac:
            print('old_mac -> ' + str(old_mac))
            print('new_mac -> ' + new_mac)
            print('Setting new mac address...')
            se = '$wlanmac,S,' + new_mac + str('\r\n')
            sc.send(se.encode())
            data = sc.recv(100)
            print('data->' + str(data))
            result = data.decode().split(',')[3].find('OK')
            print('result->' + str(result))
            if result > 0:
                print('Lan Mac not set')
                return False, "Lan Mac not set"
            else:
                print('Lan Mac successfully set')
                ret = upload_file('wifi')

                print(ret)

    except OSError as err:
        print(err)
        return False, err

    # ******************************************************************************************








    def check_serial_event(self):
        global DemoJM_Serialport
        serial_thread = threading.Timer(1, self.check_serial_event)
        try:
            if DemoJM_Serialport.isOpen():
                serial_thread.start()
                print('running serial thread')
                assert isinstance(DemoJM_Serialport, serial.Serial)
                if DemoJM_Serialport.inWaiting():
                    while True:
                        c = DemoJM_Serialport.read(1)
                        print('received ' + str(c))
                        if c:
                            self.serialtrigger.emit(c)
                            break
                        else:
                            break
        except OSError as err:
            print(err)
        except ValueError as err:
            print(err)
        except SystemError as err:
            print(err)
        except NameError as err:
            print(err)

    def check_for_config(self):
        ret = fl.configfileRead('CONFIG','file_ver')
        print('Found Configuration file version ' + ret)

    def power_up_relay(self):
        print('power up power relay')
        gp.output(self.powerrelay_pin, self.gpio_on) #PIN

    def power_cycle_relay(self):
        print('power up relay')
        gp.output(self.powerrelay_pin, self.gpio_off)  ## Switch on pin 7
        time.sleep(2)
        gp.output(self.powerrelay_pin, self.gpio_on)  ## Switch on pin 7

    def power_down_relay(self):
        print('power down power relay')
        gp.output(self.powerrelay_pin, self.gpio_off)

    def reset_tfp2(self):
        pass

    def powerup_tfp3(self):
        print('power up tfp3 relay')
        gp.output(self.tfp3relay_pin, self.gpio_off)

    def powerdown_tfp3(self):
        print('power down tfp3 relay')
        gp.output(self.tfp3relay_pin, self.gpio_off)

    def adc(self):
        #TODO figure out what pin is the adc
        pass

    def all_outputs_toggle(self):
        pass

    def get_status(self):
        print('gpio get status off all pins')
        gp.output(self.gpio_tfp3relay_pin, self.gpio_off)

    def send_report(self):
        pass

    def SerialTest(self):
        data = self.lnSerialTest.text()
        print('serial test' + data)
        self.lnSerialTest.clear()
        self.parse_serial_data(data)

    def parse_serial_data(self,bData):
        strData = bData.decode('utf-8')
        global DemoJM_Serialport
        DemoJM_Serialport.write(bData + b'\r')
        self.txtSerialData.appendPlainText(strData)
        print('incoming data->' + strData)
        if (strData == 'S') or (strData == 's'):
            MainWindow.send_report()
        elif  (strData == 'L') or (strData == 'l'):
            MainWindow.limitswitch_check()
        elif (strData == 'Z') or (strData == 'z'):
            MainWindow.getstatus()
        else:
            try:
                #Send ACK to LabVIEW
                DemoJM_Serialport.write(b'K')
                DemoJM_Serialport.write(b'\r')
            except:
                print('no serial port')

        if (strData == 'P') or (strData == 'p'):
            MainWindow.power_up_relay(self)
        elif ((strData == 'C') or (strData == 'c')):
            MainWindow.power_cycle_relay(self)
        elif ((strData == 'G') or (strData == 'g')):
            MainWindow.programCyclone
        elif ((strData == 'D') or (strData == 'd')):
            MainWindow.power_down_relay(self)
        elif ((strData == 'R')  or (strData == 'r')):
            MainWindow.reset_tfp2(self)
        elif ((strData == 'U') or (strData == 'u')):
            MainWindow.powerup_tfp3(self)
        elif ((strData == 'O') or (strData == 'o')):
            MainWindow.powerdown_tfp3(self)
        elif ((strData == 'A') or (strData == 'a')):
            MainWindow.adc(self)
        elif ((strData == 'W') or (strData == 'w')):
            MainWindow.all_outputs_toggle()

    def GetVoltages(self):
        global ip_address
        print("Pressed voltage...")
        data = el.getvoltages(ip_address)
        print(data)

    def pressedSendSerialButton(self):
        print("Pressed Serial Send")

    def pressedTFP3Button(self):
        self.lblStatus.setText("TFP3 programming...")
        print('Starting TFP3 programmer on port ' + tfp3_serial_port)
        ret = pl.TFP3Program(tfp3_serial_port)
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
        if ret[0]:
            pass
        else:
            pass

    def programCyclone(self):
        self.lblStatus.setText("Programming cyclone !")
        print("Programming cyclone !")
        ret = pl.CycloneProgram(cyclone_serial_port)
        print ('Returned value '+ str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
        if ret[0]:
            pass
        else:
            pass


    def pressedSendScannerButton(self):
        print("Pressed Scanner Send")
        ret = ml.ScanBarcode(scanner_serial_port)
        print('Received from scanner: '+ str(ret[0]))

        if ret:
            pass
        else:
            pass

    def pressedTelnetButton(self):
        print("Pressed Telnet")

    def PingUUT(self):
        ret = el.pinguut(ip_address, 5)
        print('Returned value ' + str(ret[0]))
        #self.lblStatus.setText(str(ret[1]))
        if ret[0]:
            pass
        else:
            pass

    def tfp3SerialPortChanged(self):
        global tfp3_serial_port
        tfp3_serial_port = self.cbTFP3ComPort.currentText()
        fl.configfileWrite('TFP3','COM_PORT',tfp3_serial_port)
        print('TFP3 port changed to  ' + tfp3_serial_port)

    def ScannerSerialPortChanged(self):
        global scanner_serial_port
        scanner_serial_port = self.cbScannerComPort.currentText()
        fl.configfileWrite('SCANNER','COM_PORT',scanner_serial_port)
        print('Scanner port changed to '+ scanner_serial_port )

    def CycloneSerialPortChanged(self):
        global cyclone_serial_port
        cyclone_serial_port = self.cbCycloneComPort.currentText()
        fl.configfileWrite('CYCLONE','COM_PORT',cyclone_serial_port)
        print('Cyclone port changed to ' + cyclone_serial_port)

    def ModbusSerialPortChanged(self):
        global modbus_serial_port
        modbus_serial_port = self.cbModbusComPort.currentText()
        fl.configfileWrite('MODBUS','COM_PORT',modbus_serial_port)
        print('Modbus port changed to ' + modbus_serial_port)

    def DemoJMSerialPortChanged(self):
        global demojm_serial_port
        demojm_serial_port = self.cbDemoJMComPort.currentText()
        fl.configfileWrite('DEMOJM', 'COM_PORT', demojm_serial_port)
        print('DemoJM port changed to ' + demojm_serial_port)
        global DemoJM_Serialport
        try:
            DemoJM_Serialport = serial.Serial(demojm_serial_port, baudrate=115200, timeout=10,
                                              parity=serial.PARITY_NONE,
                                              stopbits=serial.STOPBITS_ONE,
                                              bytesize=serial.EIGHTBITS
                                              )
            print('Opened demojm serial port on port ' + demojm_serial_port)
            self.check_serial_event()

        except OSError as err:
            print(err)
        except ValueError as err:
            print(err)
        except SystemError as err:
            print(err)
        except NameError as err:
            print(err)

    def populate_defaults(self):
        global tfp3_serial_port
        global scanner_serial_port
        global cyclone_serial_port
        global modbus_serial_port
        global demojm_serial_port
        global DemoJM_Serialport
        global ip_address

        print('Populating defaults...')

        ip_address = fl.configfileRead('TELNET','ip_address')

        tfp3_serial_port = fl.configfileRead('TFP3', 'COM_PORT')
        index = self.cbTFP3ComPort.findText(tfp3_serial_port)
        if index >= 0:
            self.cbTFP3ComPort.setCurrentIndex(index)
        else:
            index = self.cbTFP3ComPort.findText('none')
            self.cbTFP3ComPort.setCurrentIndex(index)

        scanner_serial_port = fl.configfileRead('SCANNER', 'COM_PORT')
        index = self.cbScannerComPort.findText(scanner_serial_port)
        if index >=0:
            self.cbScannerComPort.setCurrentIndex(index)
        else:
            index = self.cbScannerComPort.findText('none')
            self.cbScannerComPort.setCurrentIndex(index)

        cyclone_serial_port = fl.configfileRead('CYCLONE', 'COM_PORT')
        index = self.cbCycloneComPort.findText(cyclone_serial_port)
        if index >=0:
            self.cbCycloneComPort.setCurrentIndex(index)
        else:
            index = self.cbCycloneComPort.findText('none')
            self.cbCycloneComPort.setCurrentIndex(index)


        modbus_serial_port = fl.configfileRead('MODBUS', 'COM_PORT')
        index = self.cbModbusComPort.findText(modbus_serial_port)
        if index >=0:
            self.cbModbusComPort.setCurrentIndex(index)
        else:
            index = self.cbModbusComPort.findText('none')
            self.cbModbusComPort.setCurrentIndex(index)

        demojm_serial_port = fl.configfileRead('DEMOJM', 'COM_PORT')
        index = self.cbDemoJMComPort.findText(demojm_serial_port)
        if index >=0:
            self.cbDemoJMComPort.setCurrentIndex(index)
        else:
            index = self.cbDemoJMComPort.findText('none')
            self.cbDemoJMComPort.setCurrentIndex(index)


def main():

    import sys
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
