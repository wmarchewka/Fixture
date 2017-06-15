import time
import os
import minimalmodbus
import serial
import serial.tools.list_ports
import FileConfigurationLibrary as fl

# ******************************************************************************************
class SCML(object):
    def __init__(self):
        pass

    def collectSerialPorts(self):
        port_modbus = ''
        port_modbus_description = ''
        port_tfp3 = ''
        port_tfp3_description = ''
        port_cyclone = ''
        port_cyclone_description = ''
        port_scanner = ''
        port_scanner_description = ''
        port_demojm = ''
        port_demojm_description = ''
        ports = list(serial.tools.list_ports.comports())
        devices = []
        device_descriptions = []
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
            device_descriptions.append(p.description)

            try:
                if fl.configfileRead('MODBUS','COM_DESCRIPTION') == 'None':
                    if p.description.find('RS485') >= 0 or p.hwid.find('0403:6001') >= 0:
                        port_modbus = p.device
                        port_modbus_description = p.description
                        fl.configfileWrite('MODBUS','COM_PORT', port_modbus)
                        fl.configfileWrite('MODBUS', 'COM_DESCRIPTION', port_modbus_description)
            except AttributeError as err:
                pass

            try:
                if fl.configfileRead('TFP3','COM_DESCRIPTION') == 'None':
                    if p.description.find('MAXQ') >= 0:
                        port_tfp3 = p.device
                        port_tfp3_description = p.description
                        fl.configfileWrite('TFP3','COM_PORT', port_tfp3)
                        fl.configfileWrite('TFP3', 'COM_DESCRIPTION', port_tfp3_description)
            except AttributeError as err:
                pass

            try:
                if fl.configfileRead('SCANNER','COM_DESCRIPTION') == 'None':
                    if p.manufacturer.find('Honeywell') >= 0:
                        port_scanner = p.device
                        port_scanner_description = p.description
                        fl.configfileWrite('SCANNER', 'COM_PORT', port_scanner)
                        fl.configfileWrite('SCANNER', 'COM_DESCRIPTION', port_scanner_description)
            except AttributeError as err:
                pass

            try:
                if fl.configfileRead('CYCLONE', 'COM_DESCRIPTION') == 'None':
                    if p.description.find('USB-Serial Controller') >= 0:
                        if p.manufacturer.find('Prolific') >= 0:
                            port_cyclone = p.device
                            port_cyclone_description = p.description
                            fl.configfileWrite('CYCLONE', 'COM_PORT', port_cyclone)
                            fl.configfileWrite('CYCLONE', 'COM_DESCRIPTION', port_cyclone_description)
                    if p.serial_number.find('FT0DICBKA') >= 0:
                        port_cyclone = p.device
                        port_cyclone_description = p.description
                        fl.configfileWrite('CYCLONE','COM_PORT', port_cyclone)
                        fl.configfileWrite('CYCLONE', 'COM_DESCRIPTION', port_cyclone_description)
            except AttributeError as err:
                pass

            try:
                if fl.configfileRead('DEMOJM', 'COM_DESCRIPTION') == 'None':
                    if p.description.find('USB-Serial Controller') >= 0:
                        if p.manufacturer.find('Prolific') >= 0:
                            port_demojm = p.device
                            port_demojm_description = p.description
                            fl.configfileWrite('DEMOJM', 'COM_PORT', port_demojm)
                            fl.configfileWrite('DEMOJM', 'COM_DESCRIPTION', port_demojm_description)
            except AttributeError as err:
                pass
        devices.append("None")
        device_descriptions.append("None")
        self.lblStatus.setText('Serial scan complete...')
        print('Serial scan complete...')
        return True, devices, device_descriptions, port_modbus, port_modbus_description, \
               port_tfp3, port_tfp3_description, \
               port_cyclone, port_cyclone_description, \
                port_scanner, port_scanner_description, \
                port_demojm, port_demojm_description

     # ******************************************************************************************
    def MajorBoardType(self, p_number, board_type, config_cal):

        #TODO: need to finish this
        print('MAJOR BOARD TYPE')
        fn = os.path.dirname(__file__)
        fn = str(fn) + str('/SupportFiles/Board_Part_numbers.txt')
        print(fn)
        searchstring = p_number + '-' + board_type
        searchstring = searchstring[1:10]
        print('Searching for ' + searchstring)
        with open(fn) as board_name_table:
            for line in board_name_table:
                print('line read->' + line)
                found = line.find(searchstring,1)
                if found == -1:
                    print('Not Found')
                else:
                    print('Found ->' + str(line))
                    line = line.split('\t')
                    print('line 0->' + line[0], 'line 1->' + line[1])
                    board_name = line[1]
        major_board_type = 'unknown'
        board_voltage = 'unknown'
        if p_number == 'P22276' or 'R22276':
            if board_type == '156':
                major_board_type = 'M40'
                if config_cal == '102':
                    board_voltage = 'HIGH'
            return major_board_type, board_voltage, board_name
            if board_type == '198':
                major_board_type = 'M50'
                if config_cal == '201':
                    board_voltage = 'HIGH'
            return major_board_type, board_voltage, board_name
        else:
            return major_board_type, board_voltage, board_name
    # ******************************************************************************************
    def ScanBarcode(self, simulate, port, max):

        major_board_type = ''
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

        if port == 'None':
            self.lblStatus.setText('Please select Barcode serial port')
            return False, 'Please select Barcode serial port'
        print('Looking for barcode scanner...')
        time.sleep(1)
        self.lblStatus.setText('Looking for barcode scanner...')
        ser = serial.Serial(port, 115200, timeout=1)
        print('Found barcode scanner on port ' + ser.name)
        self.lblStatus.setText('Found barcode scanner on port ' + ser.name)
        while count < max:
            try:
                ser.write(b'\x16T\r')  # write trigger
                print('Sending trigger  \x16T\r')
                # TODO: make sure this isnt blocking and contains enough characters read
                line = ser.read(38)  # check for return data
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
                    print('Failed to scan. Retrying ' + str(count))
                    self.lblStatus.setText('Failed to scan. Retrying ' + str(count))
                    time.sleep(1.0)
                    count = count + 1
                else:
                    ser.close()
                    print('Data returned from scanner')
                    nodashes = str(line).split('-')
                    print("No dashes->" + str(nodashes))
                    p_number = nodashes[0]
                    board_type = nodashes[1]
                    config_cal = nodashes[2]
                    unknown = nodashes[3]
                    revision = nodashes[4]
                    solder_type = nodashes[5]
                    build_date = nodashes[6]
                    serial_number = nodashes[7]
                    firmware = nodashes[8]

                    print('P Number     ->' + str(p_number))
                    print('Board Type   ->' + str(board_type))
                    print('Config Cal   ->' + str(config_cal))
                    print('Unknown      ->' + str(unknown))
                    print('Revision     ->' + str(revision))
                    print('Solder Type  ->' + str(solder_type))
                    print('Build Date   ->' + str(build_date))
                    print('Serial number->' + str(serial_number))
                    print('Firmware     ->' + str(firmware))
                    partnumber = p_number + '-' + board_type + '-' + config_cal + '-' + \
                                 unknown + '-' + revision + '-' + solder_type + '-' + build_date + '-' + \
                                 serial_number + '-'  + firmware
                    filename = partnumber + '.txt'
                    ret_value = SCML.MajorBoardType(self, p_number, board_type, config_cal)
                    major_board_type = ret_value[0]
                    board_voltage = ret_value[1]
                    board_name = ret_value[2]
                    print('Filename ' + filename)
                    fl.configfileWrite('UUT', 'PART_NUMBER', partnumber)
                    fl.configfileWrite('UUT', 'P_NUMBER', p_number)
                    fl.configfileWrite('UUT', 'BOARD', board_type)
                    fl.configfileWrite('UUT', 'CONFIG_CAL', config_cal)
                    fl.configfileWrite('UUT', 'UNKNOWN', unknown)
                    fl.configfileWrite('UUT', 'REVISION', revision)
                    fl.configfileWrite('UUT', 'SOLDER_TYPE', solder_type)
                    fl.configfileWrite('UUT', 'BUILD_DATE', build_date)
                    fl.configfileWrite('UUT', 'SERIAL_NUMBER', serial_number)
                    fl.configfileWrite('UUT', 'MAJOR_BOARD_TYPE', major_board_type)
                    fl.configfileWrite('UUT', 'BOARD_VOLTAGE', board_voltage)
                    fl.configfileWrite('UUT', 'BOARD_NAME', board_name)

                    fl.logfileWrite(filename, 'BOARD', 'part_number', filename)
                    fl.logfileWrite(filename, 'BOARD', 'p_number', p_number)
                    fl.logfileWrite(filename, 'BOARD', 'board_type', board_type)
                    fl.logfileWrite(filename, 'BOARD', 'config_cal', config_cal)
                    fl.logfileWrite(filename, 'BOARD', 'unknown', unknown)
                    fl.logfileWrite(filename, 'BOARD', 'revision', revision)
                    fl.logfileWrite(filename, 'BOARD', 'solder_type', solder_type)
                    fl.logfileWrite(filename, 'BOARD', 'build_date', build_date)
                    fl.logfileWrite(filename, 'BOARD', 'serial_number', serial_number)
                    fl.logfileWrite(filename, 'BOARD', 'board_major_type', major_board_type)
                    fl.logfileWrite(filename, 'UUT', 'board_voltage', board_voltage)
                    fl.logfileWrite(filename, 'UUT', 'board_name', board_name)
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
                    print('BOARD', 'solder_type', solder_type)
                    print('BOARD', 'build date', build_date)
                    print('BOARD', 'serial_number', serial_number)
                    print('BOARD', 'board_major_type', major_board_type)
                    print('BOARD', 'board_voltage', board_voltage)
                    print('BOARD', 'board_name', board_name)
                    print('BOARD', 'k60_firmware_version',
                          fl.configfileRead('M40_FIRMWARE', 'm40_k60_firmware_version'))
                    print('BOARD', 'web_page_version',
                          fl.configfileRead('M40_FIRMWARE', 'm40_web_page_firmware_version'))
                    print('BOARD', 'meter_ic_version',
                          fl.configfileRead('M40_FIRMWARE', 'm40_meter_ic_firMware_version'))
                    print('BOARD', 'wifi_firmware_version',
                          fl.configfileRead('M40_FIRMWARE', 'm40_meter_ic_firmware_version'))
                    print('TEST_DATE_TIME', 'test_time', time.strftime('%H:%M:%S'))
                    print('TEST_DATE_TIME', 'test_date', time.strftime('%m:%d:%Y'))
                    return True, str(line)

            except IndexError as err:
                print(err)
                return False, "Barcode improperly formatted"

            except OSError as err:
                print(err)
                self.lblStatus.setText(err)
                return False, err

            except Exception as err:
                print(err)
                self.lblStatus.setText(err)
                return False, err

        ser.close()
        self.lblStatus.setText('Failed to scan')
        return False, ('Failed to scan')

    # ******************************************************************************************
    def mbComm(self, port, address, register, type, num_of_regs, write, writevalue):

        #type 0 = int 1 = float  2 = ascii

        if port == '':
            self.lblStatus.setText('Please select Modbus serial port')
            return False, 'Please select Modbus serial port'

        try:
            address = fl.configfileRead('MODBUS','slave_address')
            address= int(address)
            uut = minimalmodbus.Instrument(port, address)
            uut.debug = True
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
            if not write:
                if type == 0:
                    value = uut.read_registers(register, num_of_regs , 4 )
                    return_value = value
                if type == 1:
                    value = uut.read_float(register, num_of_regs, 4)
                    return_value = round(value,2)
                if type == 2:
                    value = uut.read_string(register, num_of_regs, 4)
                    return_value = value
                print('Value->' + str(value))
                uut.serial.close
                return True, return_value
            elif write:
                #first write Modbus acess code to register 2047 decimal
                #Admin:2570
                #Factory:3855
                uut.write_register(2047, 0)
                if type == 0:
                    uut.write_registers(register, num_of_regs, int(writevalue))
                    return True, ""
                if type == 1:
                    uut.write_float(register, float(writevalue), num_of_regs)
                    return True, ""
                if type == 2:
                    uut.write_string(register, str(writevalue), num_of_regs)
                    return True, ""


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
