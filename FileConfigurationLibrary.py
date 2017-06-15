import configparser

#******************************************************************************************
def logfileWrite(filename, section, key, value):

    old_filename = ''
    config = configparser.RawConfigParser()
    old_filename = config.read(filename)
    if old_filename == '':
        print('Creating new test record...')
    else:
        print('Test record exists. Updating existing record.')

    try:
        print('Writing to ' + filename + '->Section:' + section + 'Key:' + key + ' Value: ' + value)
        config.add_section(section)
        config.set(section, key, value)
        with open(filename, 'w') as configfile:
            config.write(configfile)
    except:
        print('Writing to ' + filename + '->Section:' + section + ' Key:' + key + ' Value: ' + value)
        config.set(section, key, value)
        with open(filename, 'w') as configfile:
            config.write(configfile)

#******************************************************************************************
def logfileWriteDefaults():

    try:
        config = configparser.RawConfigParser()
        config.read('master_logfile.cfg')
        print(config)

        config.add_section('BOARD')
        config.set('BOARD', 'part_number', '')
        config.set('BOARD', 'p_number', '')
        config.set('BOARD', 'board_type', '')
        config.set('BOARD', 'config_cal', '')
        config.set('BOARD', 'unknown', '')
        config.set('BOARD', 'revision', '')
        config.set('BOARD', 'solder_type', '')
        config.set('BOARD', 'build_date', '')
        config.set('BOARD', 'serial_number', '')
        config.set('BOARD', 'firmware', '')
        config.set('BOARD', 'board_major_type', '')
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
#******************************************************************************************
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
        config.set('CYCLONE', 'COM_DESCRIPTION', 'DESCRIPTION')
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
        config.set('M40_FOLDERS', 'M40_FIRMWARE', 'C:\\UEC\\Functional Test\\M40\\Configuration\\firmware_v3.39.bin')
        config.set('M40_FOLDERS', 'M40_WIFI_FIRMWARE', 'C:\\UEC\\Functional Test\\M40\\Configuration\\wifi_v0x2124a503.bin')
        config.set('M40_FOLDERS', 'M40_WEB_PAGE_UPLOAD', 'C:\\UEC\\Functional Test\\M40\\Configuration\\web_pages_UEC025_ENG.tfs')
        config.set('M40_FOLDERS', 'M40_METER_IC_FIRMWARE', 'C:\\UEC\\Functional Test\\M40\\Configuration\\meter_v1.20.hex')
        config.add_section('M50_FOLDERS')
        config.set('M50_FOLDERS', 'M50_BASE', 'C:\\UEC\\Functional Test\\M50')
        config.set('M50_FOLDERS', 'M50_TEST_REPORTS', 'C:\\UEC\\Functional Test\\M50\\Test Reports\\')
        config.set('M50_FOLDERS', 'M50_CONFIGURATION', 'C:\\UEC\\Functional Test\\M50\\Configuration\\')
        config.set('M50_FOLDERS', 'M50_MASTER_TEST_REPORT', 'C:\\UEC\\Functional Test\\M50\\Test Reports\\Dual Ethernet\\')
        config.set('M50_FOLDERS', 'M50_MASTER_TEST_REPORT', 'C:\\UEC\\Functional Test\\M50\\Test Reports\\Dual Ethernet\\')
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

#******************************************************************************************
def configfileWrite(section,key,value):

    value = str(value)
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

#******************************************************************************************
def configfileRead(section,key):
    config = configparser.RawConfigParser()
    config.read('configuration.cfg')
    try:
        value = config.get(section,key)
        print('Reading from config-> Section:' + section + ' Key:' + key + ' Value: ' + value)
        return value
    except:
        return ('ERROR')

#******************************************************************************************
def main():
    configfileWriteDefaults()

if __name__ == '__main__':
    main()