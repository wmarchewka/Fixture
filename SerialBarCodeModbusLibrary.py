import glob
import time
import sys

import minimalmodbus
import serial
import serial.tools.list_ports
import FileConfigurationLibrary as fl


class SCML(object):
    def __init__(self):
        pass

# ******************************************************************************************
    def collectSerialPorts(self):

        port_modbus = ''
        port_tfp3 = ''
        port_cyclone = ''
        port_scanner = ''
        port_demojm = ''
        ports = list(serial.tools.list_ports.comports())
        devices = []
        for p in ports:
            print('-----------------------------------------')
            print(p)
            print('description->' + str(p.description))
            print('devicestr(' + str(p.device))
            print('hwidstr(' + str(p.hwid))
            print('interfacestr(' + str(p.interface))
            print('locationstr(' + str(p.location))
            print('maufacturerstr(' + str(p.manufacturer))
            print('namestr(' + str(p.name))
            print('pidstr(' + str(p.pid))
            print('product->' + str(p.product))
            print('serial number->' + str(p.serial_number))
            print('vid->' + str(p.vid))
            self.lblStatus.setText('Found ->' + str(p.device))
            devices.append(p.device)

            try:
                if p.description.find('RS485') >= 0 or p.hwid.find('0403:6001') >= 0:
                    port_modbus = p.device
                    fl.configfileWrite('MODBUS','com_port', port_modbus)
            except AttributeError as err:
                pass

            try:
                if p.description.find('MAXQ') >= 0:
                    port_tfp3 = p.device
                    fl.configfileWrite('TFP3','com_port', port_modbus)
            except AttributeError as err:
                pass

            try:
                if p.manufacturer.find('Honeywell') >= 0:
                    port_scanner = p.device
                    fl.configfileWrite('SCANNER','com_port', port_modbus)
            except AttributeError as err:
                pass

            try:
                if p.description.find('USB-Serial Controller') >= 0:
                    if p.manufacturer.find('Prolific') >= 0:
                        port_cyclone = p.device
                        fl.configfileWrite('CYCLONE', 'com_port', port_modbus)
                if p.serial_number.find('FT0DICBKA') >= 0:
                    port_cyclone = p.device
                    fl.configfileWrite('CYCLONE','com_port', port_modbus)
            except AttributeError as err:
                pass

            try:
                if p.description.find('USB-Serial Controller') >= 0:
                    if p.manufacturer.find('Prolific') >= 0:
                        port_demojm = p.device
                        fl.configfileWrite('DEMOJM', 'com_port', port_modbus)
            except AttributeError as err:
                pass
        self.lblStatus.setText('Serial scan complete...')
        print('Serial scan complete...')
        return True, devices, port_modbus, port_tfp3, port_scanner, port_cyclone, port_demojm

     # ******************************************************************************************
    def MajorBoardType(self, p_number, board_type, config_cal):
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

    # ******************************************************************************************
    def ScanBarcode(self, simulate, port, max):
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
        count = 0

        print(simulate)

        if port == '':
            self.lblStatus.setText('Please select Barcode serial port')
            return False, 'Please select Barcode serial port'

        while count < max:
            try:
                print('Looking for barcode scanner...')  # check which port was really used
                self.lblStatus.setText('Looking for barcode scanner...')
                ser = serial.Serial(port, 115200, timeout=1)
                print('Found barcode scanner on port ' + ser.name)
                ser.write(b'\x16T\r')  # write trigger
                print('Sending trigger  \x16T\r')
                # TODO: make sure this isnt blocking and contains enough characters read
                line = ser.read(30)  # check for return data
                ser.write(b'\x16U\r')  # send off trigger
                line = line.decode('ascii')
                print(line)
                self.lblStatus.setText(line)
                self.lblCurrentSerialNumber.setText(line)

            except OSError as err:
                print('OSError ' + str(err))
                self.lblStatus.setText(err)
                return False, err

            except Exception as err:
                print('Exceptopn ' + str(err))
                self.lblStatus.setText(err)
                return False, err

            try:
                if not line:
                    count = count + 1
                    print('Failed to scan. Retrying ' + str(count))
                    self.lblStatus.setText('Failed to scan. Retrying ' + str(count))
                    time.sleep(0.5)
                    ser.close()
                else:
                    ser.close()
                    print('Data returned from scanner')
                    nodashes = str(line).split('-')
                    print(nodashes)
                    spaces = nodashes[3]
                    nospaces = spaces.split()
                    print(nospaces)
                    p_number = nodashes[0]
                    board_type = nodashes[1]
                    config_cal = nodashes[2]
                    unknown = nospaces[0]
                    revision = nospaces[1]
                    build_date = nospaces[2]
                    serial_number = nospaces[3]
                    partnumber = p_number + '-' + board_type + '-' + config_cal + '-' + unknown + '-' + revision + '-' + build_date + '-' + serial_number
                    filename = partnumber + '.txt'
                    SCML.MajorBoardType(p_number, board_type, config_cal)
                    print('Filename ' + filename)
                    fl.configfileWrite('UUT', 'PART_NUMBER', partnumber)
                    fl.configfileWrite('UUT', 'P_NUMBER', p_number)
                    fl.configfileWrite('UUT', 'BOARD', board_type)
                    fl.configfileWrite('UUT', 'CONFIG_CAL', config_cal)
                    fl.configfileWrite('UUT', 'UNKNOWN', unknown)
                    fl.configfileWrite('UUT', 'REVISION', revision)
                    fl.configfileWrite('UUT', 'BUILD_DATE', build_date)
                    fl.configfileWrite('UUT', 'SERIAL_NUMBER', serial_number)
                    fl.configfileWrite('UUT', 'MAJOR_BOARD_TYPE', major_board_type)
                    fl.configfileWrite('UUT', 'BOARD_VOLTAGE', board_voltage)

                    fl.logfileWrite(filename, 'BOARD', 'part_number', filename)
                    fl.logfileWrite(filename, 'BOARD', 'p_number', p_number)
                    fl.logfileWrite(filename, 'BOARD', 'board type', board_type)
                    fl.logfileWrite(filename, 'BOARD', 'config calibration', config_cal)
                    fl.logfileWrite(filename, 'BOARD', 'unknown', unknown)
                    fl.logfileWrite(filename, 'BOARD', 'revision', revision)
                    fl.logfileWrite(filename, 'BOARD', 'build data', build_date)
                    fl.logfileWrite(filename, 'BOARD', 'serial_number', serial_number)
                    fl.logfileWrite(filename, 'BOARD', 'board_major_type', major_board_type)
                    fl.logfileWrite(filename, 'BOARD', 'k60_firmware_version',
                                    fl.configfileRead('M40_FIRMWARE', 'm40_k60_firmware_version'))
                    fl.logfileWrite(filename, 'BOARD', 'web_page_version',
                                    fl.configfileRead('M40_FIRMWARE', 'm40_web_page_firmware_version'))
                    fl.logfileWrite(filename, 'BOARD', 'meter_ic_version',
                                    fl.configfileRead('M40_FIRMWARE', 'm40_meter_ic_firMware_version'))
                    fl.logfileWrite(filename, 'BOARD', 'wifi_firmware_version',
                                    fl.configfileRead('M40_FIRMWARE', 'm40_meter_ic_firmware_version'))
                    fl.logfileWrite(filename, 'TEST_DATE_TIME', 'test_time', time.strftime('%H:%M:%S'))
                    fl.logfileWrite(filename, 'TEST_DATE_TIME', 'test_date', time.strftime('%d:%m:%Y'))
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
                          fl.configfileRead('M40_FIRMWARE', 'm40_k60_firmware_version'))
                    print('BOARD', 'web_page_version',
                          fl.configfileRead('M40_FIRMWARE', 'm40_web_page_firmware_version'))
                    print('BOARD', 'meter_ic_version',
                          fl.configfileRead('M40_FIRMWARE', 'm40_meter_ic_firMware_version'))
                    print('BOARD', 'wifi_firmware_version',
                          fl.configfileRead('M40_FIRMWARE', 'm40_meter_ic_firmware_version'))
                    print('TEST_DATE_TIME', 'test_time', time.strftime('%H:%M:%S'))
                    print('TEST_DATE_TIME', 'test_date', time.strftime('%d:%m:%Y'))
                    return True, str(line)

            except OSError as err:
                print(err)
                self.lblStatus.setText(err)
                return False, err

            except Exception as err:
                print(err)
                self.lblStatus.setText(err)
                return False, err

        self.lblStatus.setText('Failed to scan')
        return False, ('Failed to scan')

    # ******************************************************************************************
    def mbComm(self, port, address, register):
        if port == '':
            self.lblStatus.setText('Please select Modbus serial port')
            return False, 'Please select Modbus serial port'

        try:
            address = fl.configfileRead('MODBUS','slave_address')
            address= int(address)
            uut = minimalmodbus.Instrument(port, address)
            uut.debug = False
            timeout = int(fl.configfileRead('MODBUS','time_out'))
            uut.serial.timeout = timeout / 1000
            uut.serial.bytesize = int(fl.configfileRead('MODBUS','data_bits'))
            parity = fl.configfileRead('MODBUS', 'parity')
            if parity == 'NONE':
                uut.serial.parity = minimalmodbus.serial.PARITY_NONE
            if parity == 'EVEN':
                uut.serial.parity = minimalmodbus.serial.PARITY_EVEN
            if parity == 'ODD':
                uut.serial.parity = minimalmodbus.serial.PARITY_ODD
            uut.serial.baudrate = int(fl.configfileRead('MODBUS','baud_rate'))
            uut.serial.stopbits = int(fl.configfileRead('MODBUS','stop_bits'))
            uut.mode = minimalmodbus.MODE_RTU
            uut.close_port_after_each_call = False
            count = 0
            while count < 1:
                # value = uut.read_register(register, 1, 4)     #register, number of decimals
                value = uut.read_float(register)  # register, number of decimals
                print('Value->' + str(value))
                time.sleep(0.200)
                count = count + 1
            uut.serial.close
            return True, round(value,2)

        except TimeoutError as err:
            print(err)
            return False, err

        except Exception as err:
            print(err)
            return False, err

        except OSError as err:
            print(err)
            return False, err

        except IOError as err:
            print(err)
            return False, err

        except ValueError as err:
            print(err)
            return False, err


    # ******************************************************************************************
def main(self):
    module = 'A'

    host_address = 1
    comport = 'COM44'
    # comport = '/dev/tty.usbserial-FT084UEL'
    register = 490

    if module == "A":
        ret = SCML.mbComm(comport, host_address, register)

    if module == "B":
        global port
        port = 'COM4'
        # port ='/dev/tty.usbmodem14444331'
        ret = SCML.ScanBarcode(port)

    if module == "C":
        ret = SCML.collectSerialPorts()

    print(ret)


# ******************************************************************************************
if __name__ == '__main__':
    main()
