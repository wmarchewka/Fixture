import configparser
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('log_filename.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
#******************************************************************************************
def configfileWriteDefaults():

    try:
        config = configparser.RawConfigParser()
        config.read('master_configuration.cfg')
        print(config)

        config.add_section('CONFIG')
        config.set('CONFIG', 'FILE_VER', '1')
        config.add_section('DEMOJM')
        config.set('DEMOJM', 'COM_PORT')
        config.set('DEMOJM', 'COM_DESCRIPTION')
        config.add_section('SCANNER')
        config.set('SCANNER', 'COM_PORT')
        config.set('SCANNER', 'COM_DESCRIPTION')
        config.add_section('CYCLONE')
        config.set('CYCLONE', 'COM_PORT')
        config.set('CYCLONE', 'COM_DESCRIPTION')
        config.add_section('TFP3')
        config.set('TFP3', 'COM_PORT')
        config.set('TFP3', 'COM_DESCRIPTION')
        config.add_section('MODBUS')
        config.set('MODBUS', 'COM_PORT')
        config.set('MODBUS', 'COM_DESCRIPTION')
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
        config.set('M40_FOLDERS', 'M40_BASE', "C:\\UEC\\Functional Test\\M40")
        config.set('M40_FOLDERS', 'M40_TEST_REPORTS', 'C:\\UEC\\Functional Test\\M40\\Test Reports\\Dual Ethernet')
        config.set('M40_FOLDERS', 'M40_CONFIGURATION', 'C:\\UEC\\Functional Test\\M40\\Configuration')
        config.set('M40_FOLDERS', 'M40_FIRMWARE', 'C:\\UEC\\Functional Test\\M40\\Configuration\\firmware_v3.39.bin')
        config.set('M40_FOLDERS', 'M40_WIFI_FIRMWARE', 'C:\\UEC\\Functional Test\\M40\\Configuration\\wifi_v0x2124a503.bin')
        config.set('M40_FOLDERS', 'M40_WEB_PAGE_UPLOAD', 'C:\\UEC\\Functional Test\\M40\\Configuration\\web_pages_UEC025_ENG.tfs')
        config.set('M40_FOLDERS', 'M40_METER_IC_FIRMWARE', 'C:\\UEC\\Functional Test\\M40\\Configuration\\meter_v1.20.hex')
        config.set('M40_FOLDERS', 'M40_MASTER_TEST_REPORT', 'C:\\UEC\\Functional Test\\M40\\Test Reports\\Dual Ethernet\\')
        config.add_section('M50_FOLDERS')
        config.set('M50_FOLDERS', 'M50_BASE', 'C:\\UEC\\Functional Test\\M50')
        config.set('M50_FOLDERS', 'M50_TEST_REPORTS', 'C:\\UEC\\Functional Test\\M50\\Test Reports\\')
        config.set('M50_FOLDERS', 'M50_CONFIGURATION', 'C:\\UEC\\Functional Test\\M50\\Configuration\\')
        config.set('M50_FOLDERS', 'M50_FIRMWARE', 'C:\\UEC\\Functional Test\\M50\\Configuration\\firmware_v3.39.bin')
        config.set('M50_FOLDERS', 'M50_WIFI_FIRMWARE', 'C:\\UEC\\Functional Test\\M50\\Configuration\\wifi_v0x2124a503.bin')
        config.set('M50_FOLDERS', 'M50_WEB_PAGE_UPLOAD', 'C:\\UEC\\Functional Test\\M50\\Configuration\\web_pages_UEC025_ENG.tfs')
        config.set('M40_FOLDERS', 'M50_METER_IC_FIRMWARE', 'C:\\UEC\\Functional Test\\M50\\Configuration\\meter_v1.20.hex')
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
        config.set('UUT', 'UNKNOWN', '')
        config.set('UUT', 'REVISION', '')
        config.set('UUT', 'SOLDER_TYPE', '')
        config.set('UUT', 'BUILD_DATE', '')
        config.set('UUT', 'SERIAL_NUMBER', '')
        config.set('UUT', 'MAJOR_BOARD_TYPE', '')
        config.set('UUT', 'BOARD_VOLTAGE', '')
        config.set('UUT', 'FIRMWARE', '')
        config.set('UUT', 'BOARD_NAME', '')

        with open('master_configuration.cfg', 'w') as configfile:
            config.write(configfile)
        with open('configuration.cfg', 'w') as configfile:
            config.write(configfile)

    except Exception as err:
        print(err)



#******************************************************************************************
def main():
    ret = configfileWriteDefaults()
    print(ret)

if __name__ == '__main__':
    main()