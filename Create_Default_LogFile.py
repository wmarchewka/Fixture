import configparser

config = configparser.RawConfigParser()
config.read('master_logfile.cfg')
print(config)

def config_write_defaults():
    config.add_section('BOARD')
    config.set('BOARD', 'part_number', '')
    config.set('BOARD', 'p_number', '')
    config.set('BOARD', 'board_type', '')
    config.set('BOARD', 'config_calibration', '')
    config.set('BOARD', 'unknown', '')
    config.set('BOARD', 'revision', '')
    config.set('BOARD', 'serial_ number', '')
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

def main():
    config_write_defaults()
    pass


if __name__ == '__main__':
    main()
