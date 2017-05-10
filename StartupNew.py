# native libraries
import threading
import sys
import base64
import os
import socket
import telnetlib
import time
# other libraries
import serial

try:
    import RPi.GPIO as gp
except ImportError:
    import FakeRPi.GPIO as gp
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
# my libraries
from QT_Project import mainwindow_auto as mw
from PyQt5.QtCore import pyqtSignal
import SerialBarCodeModbusLibrary as ml
import ProgrammersLibrary as pl
import EthernetCommLibrary as el
import FileConfigurationLibrary as fl
import SupportLibrary as sl

global demojm_serial_port
global Testing


class MainWindow(QMainWindow, mw.Ui_MainWindow):
    global DemoJM_Serialport
    serialtrigger = pyqtSignal(bytes)

    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file

        # setup serial triiger
        self.serialtrigger.connect(self.parse_serial_data)

        # setup button signals
        self.pbPowerOn.clicked.connect(self.power_up_relay)
        self.pbPowerOff.clicked.connect(self.power_down_relay)
        self.pbButtonTest.clicked.connect(self.button_buttontest)
        self.pbTelnetGetVoltages.clicked.connect(self.button_voltages)
        self.pbReadScanner.clicked.connect(self.button_scanner)
        self.pbDoPing.clicked.connect(self.button_ping)
        self.pbProgCyclone.clicked.connect(self.button_cyclone)
        self.pbProgTFP3.clicked.connect(self.button_tfp3)
        self.pbResetTest.clicked.connect(self.button_reset)
        self.pbWriteLanMac.clicked.connect(self.button_lanmac)
        self.pbWriteWifiMac.clicked.connect(self.button_wifimac)
        self.pbModbusInit.clicked.connect(self.button_modbusinit)
        self.pbSetPCR.clicked.connect(self.button_setpcr)
        self.pbWriteSerialNumber.clicked.connect(self.button_writeserialnummber)
        self.pbUploadFile.clicked.connect(self.button_uploadfile)
        self.pbWriteScript.clicked.connect(self.button_writescript)
        self.pbWebpageVersion.clicked.connect(self.button_webpageversion)
        self.pbSetupWIFI.clicked.connect(self.button_setupwifi)

        # setup combobox change signals
        self.cbTFP3ComPort.currentIndexChanged.connect(self.tfp3SerialPortChanged)
        self.cbScannerComPort.currentIndexChanged.connect(self.ScannerSerialPortChanged)
        self.cbCycloneComPort.currentIndexChanged.connect(self.CycloneSerialPortChanged)
        self.cbModbusComPort.currentIndexChanged.connect(self.ModbusSerialPortChanged)
        self.cbDemoJMComPort.currentIndexChanged.connect(self.DemoJMSerialPortChanged)
        self.cbDemoJMComPort.activated[str].connect(self.DemoJMSerialPortChanged)

        # setup combobox change signals
        self.lnSerialTest.textChanged.connect(self.SerialTest)

        # look to ensure we have a configuration file
        self.check_for_config()  # open configuration file

        # do all initializtion
        self.populate_defaults()
        print('TFP3 relay pin ' + str(sl.gpio_tfp3relay_pin))

        # check srial event thread
        self.check_serial_event()

    def check_serial_event(self):
        print('Starting serial receive thread')
        global DemoJM_Serialport
        serial_thread = threading.Timer(1, self.check_serial_event)
        try:
            if DemoJM_Serialport.isOpen():
                serial_thread.start()
                print('Running serial thread')
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
            print('Serial thread not running due to ' + str(err))
        except ValueError as err:
            print('Serial thread not running due to ' + str(err))
        except SystemError as err:
            print('Serial thread not running due to ' + str(err))
        except NameError as err:
            print('Serial thread not running due to ' + str(err))

    def check_for_config(self):
        ret = fl.configfileRead('CONFIG', 'file_ver')
        print('Found Configuration file version ' + ret)

    def power_up_relay(self):
        print('power up power relay')
        gp.output(self.powerrelay_pin, self.gpio_on)  # PIN

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
        # TODO figure out what pin is the adc
        pass

    def all_outputs_toggle(self):
        pass

    def get_status(self):
        print('gpio get status off all pins')
        gp.output(self.gpio_tfp3relay_pin, self.gpio_off)

    def send_report(self):
        pass

    def SerialTest(self):
        'used to simulate receiving commands from labview'
        data = self.lnSerialTest.text()
        print('serial test' + data)
        self.lnSerialTest.clear()
        self.parse_serial_data(data)

    def parse_serial_data(self, bData):
        strData = bData.decode('utf-8')
        global DemoJM_Serialport
        DemoJM_Serialport.write(bData + b'\r')
        self.txtSerialData.appendPlainText(strData)
        print('incoming data->' + strData)
        if (strData == 'S') or (strData == 's'):
            MainWindow.send_report()
        elif (strData == 'L') or (strData == 'l'):
            MainWindow.limitswitch_check()
        elif (strData == 'Z') or (strData == 'z'):
            MainWindow.getstatus()
        else:
            try:
                # Send ACK to LabVIEW
                DemoJM_Serialport.write(b'K')
                DemoJM_Serialport.write(b'\r')
            except:
                print('no serial port')

        if (strData == 'P') or (strData == 'p'):
            MainWindow.power_up_relay(self)
        elif ((strData == 'C') or (strData == 'c')):
            MainWindow.power_cycle_relay(self)
        elif ((strData == 'G') or (strData == 'g')):
            MainWindow.button_cyclone
        elif ((strData == 'D') or (strData == 'd')):
            MainWindow.power_down_relay(self)
        elif ((strData == 'R') or (strData == 'r')):
            MainWindow.reset_tfp2(self)
        elif ((strData == 'U') or (strData == 'u')):
            MainWindow.powerup_tfp3(self)
        elif ((strData == 'O') or (strData == 'o')):
            MainWindow.powerdown_tfp3(self)
        elif ((strData == 'A') or (strData == 'a')):
            MainWindow.adc(self)
        elif ((strData == 'W') or (strData == 'w')):
            MainWindow.all_outputs_toggle()

    # ****************************************************************************************************
    def button_reset(self):
        self.lblStatus.setText("Reset test...")
        print("Reset test...")
        gui_thread = threading.Thread(None, self.reset_command)
        gui_thread.start()

    # ****************************************************************************************************
    def reset_command(self):
        self.lblStatus.setText("Reset test running... !")
        time.sleep(1)
        ret = el.EthComLib.reset_button_check(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_lanmac(self):
        self.lblStatus.setText("Setting LAN MAC...")
        print("Setting LAN MAC...")
        gui_thread = threading.Thread(None, self.lanmac_command)
        gui_thread.start()

    # ****************************************************************************************************
    def lanmac_command(self):
        time.sleep(1)
        ret = el.EthComLib.lan_mac_write(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_wifimac(self):
        self.lblStatus.setText("Setting WIFI MAC...")
        print("Setting WIFI MAC...")
        gui_thread = threading.Thread(None, self.wifimac_command)
        gui_thread.start()

    # ****************************************************************************************************
    def wifimac_command(self):
        time.sleep(1)
        ret = el.EthComLib.wifi_mac_write(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_modbusinit(self):
        self.lblStatus.setText("Setting Modbus init...")
        print("Setting Modbus init...")
        gui_thread = threading.Thread(None, self.modbusinit_command)
        gui_thread.start()

    # ****************************************************************************************************
    def modbusinit_command(self):
        time.sleep(1)
        ret = el.EthComLib.modbus_init(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_setpcr(self):
        self.lblStatus.setText("Setting PCR...")
        print("Setting PCR...")
        gui_thread = threading.Thread(None, self.setpcr_command)
        gui_thread.start()

    # ****************************************************************************************************
    def setpcr_command(self):
        time.sleep(1)
        ret = el.EthComLib.pcr_write(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_writeserialnumber(self):
        self.lblStatus.setText("Setting device serial number...")
        print("Setting device serial number...")
        gui_thread = threading.Thread(None, self.writeserialnumber_command)
        gui_thread.start()

    # ****************************************************************************************************
    def writeserialnumber_command(self):
        ret = el.EthComLib.serialnumber_write(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_uploadfile(self):
        self.lblStatus.setText("Uploading file...")
        time.sleep(1)
        print("Uploading file...")
        gui_thread = threading.Thread(None, self.uploadfile_command)
        gui_thread.start()
    # ****************************************************************************************************
    def uploadfile_command(self):
        ret = el.EthComLib.fileupload(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_writescript(self):
        self.lblStatus.setText("Writing script settings...")
        time.sleep(1)
        print("Writing script settings...")
        gui_thread = threading.Thread(None, self.writescript_command)
        gui_thread.start()

    # ****************************************************************************************************
    def writescript_command(self):
        ret = el.EthComLib.script_write(self, ip_address, path)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_webpageversion(self):
        self.lblStatus.setText("Getting webpage version...")
        time.sleep(1)
        print("Getting webpage version...")
        gui_thread = threading.Thread(None, self.webpageversion_command)
        gui_thread.start()

    # ****************************************************************************************************
    def webpageversion_command(self):
        ret = el.EthComLib.webpageversion_read(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_setupwifi(self):
        self.lblStatus.setText("Setting up WIFI...")
        time.sleep(1)
        print("Getting webpage version...")
        gui_thread = threading.Thread(None, self.setupwifi_command)
        gui_thread.start()
    # ****************************************************************************************************
    def setupwifi_command(self):
        ret = el.EthComLib.wifi_setup(self, ip_address)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_voltages(self):
        global ip_address
        print("Pressed voltage...")
        gui_thread = threading.Thread(None, self.voltages_command)
        gui_thread.start()

    # ****************************************************************************************************
    def voltages_command(self):
        self.lblStatus.setText("Getting voltages...")
        ret = el.EthComLib.voltage_read(self, ip_address)
        print('Returned value ' + str(ret[1]))

    # ****************************************************************************************************
    def button_tfp3(self):
        self.lblStatus.setText("TFP3 programming...")
        print('Starting TFP3 programmer on port ' + tfp3_serial_port)
        gui_thread = threading.Thread(None, self.tftp3_command)
        gui_thread.start()

    # ****************************************************************************************************
    def tftp3_command(self):
        self.lblStatus.setText("Programming TFP3 !")
        ret = pl.TFP3Program(tfp3_serial_port)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_cyclone(self):
        print("Programming cyclone !")
        gui_thread = threading.Thread(None, self.cyclone_command)
        gui_thread.start()

    # ****************************************************************************************************
    def cyclone_command(self):
        self.lblStatus.setText("Programming cyclone !")
        ret = pl.CycloneProgram(cyclone_serial_port)
        print('Returned value ' + str(ret[1]))
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_scanner(self):
        print("Pressed Scanner button...")
        gui_thread = threading.Thread(None, self.scanner_command, None)
        gui_thread.start()

    # ****************************************************************************************************
    def scanner_command(self):
        ret = ml.SCML.ScanBarcode(self, scanner_serial_port, 5)
        print('Returned value ' + str(ret[0]))

    # ****************************************************************************************************
    def button_buttontest(self):
        print("Pressed reset button")
        gui_thread = threading.Thread(None, self.buttonttest_command, None)
        gui_thread.start()

    # ****************************************************************************************************
    def buttonttest_command(self):
        self.lblStatus.setText("Reset test running...")
        ret = el.EthComLib.m40_buttontest(self)
        print('Returned value ' + str(ret[0]))

    # ****************************************************************************************************
    def button_ping(self):
        print('Pressed ping button')
        gui_thread = threading.Thread(None, self.ping_command, None)
        gui_thread.start()

    # ****************************************************************************************************
    def ping_command(self):
        self.lblStatus.setText("Ping test running...")
        ret = el.EthComLib.pinguut(self, ip_address, 5)
        print('Returned value ' + str(ret[0]))

    # ****************************************************************************************************
    def tfp3SerialPortChanged(self):
        global tfp3_serial_port
        tfp3_serial_port = self.cbTFP3ComPort.currentText()
        fl.configfileWrite('TFP3', 'COM_PORT', tfp3_serial_port)
        print('TFP3 port changed to  ' + tfp3_serial_port)

    def ScannerSerialPortChanged(self):
        global scanner_serial_port
        scanner_serial_port = self.cbScannerComPort.currentText()
        fl.configfileWrite('SCANNER', 'COM_PORT', scanner_serial_port)
        print('Scanner port changed to ' + scanner_serial_port)

    def CycloneSerialPortChanged(self):
        global cyclone_serial_port
        cyclone_serial_port = self.cbCycloneComPort.currentText()
        fl.configfileWrite('CYCLONE', 'COM_PORT', cyclone_serial_port)
        print('Cyclone port changed to ' + cyclone_serial_port)

    def ModbusSerialPortChanged(self):
        global modbus_serial_port
        modbus_serial_port = self.cbModbusComPort.currentText()
        fl.configfileWrite('MODBUS', 'COM_PORT', modbus_serial_port)
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

        # read serial port list OS and populate comboboxes
        serial_ports_list = ml.SCML.collectSerialPorts(self)  # run serial port routine
        self.cbTFP3ComPort.addItems(serial_ports_list)
        self.cbScannerComPort.addItems(serial_ports_list)
        self.cbCycloneComPort.addItems(serial_ports_list)
        self.cbModbusComPort.addItems(serial_ports_list)
        self.cbDemoJMComPort.addItems(serial_ports_list)

        print('Populating defaults...')
        os_name = sl.getOsPlatform()
        print('os name->' + os_name)
        ip_address = fl.configfileRead('TELNET', 'ip_address')

        tfp3_serial_port = fl.configfileRead('TFP3', 'COM_PORT')
        index = self.cbTFP3ComPort.findText(tfp3_serial_port)
        if index >= 0:
            self.cbTFP3ComPort.setCurrentIndex(index)
        else:
            index = self.cbTFP3ComPort.findText('none')
            self.cbTFP3ComPort.setCurrentIndex(index)

        scanner_serial_port = fl.configfileRead('SCANNER', 'COM_PORT')
        index = self.cbScannerComPort.findText(scanner_serial_port)
        if index >= 0:
            self.cbScannerComPort.setCurrentIndex(index)
        else:
            index = self.cbScannerComPort.findText('none')
            self.cbScannerComPort.setCurrentIndex(index)

        cyclone_serial_port = fl.configfileRead('CYCLONE', 'COM_PORT')
        index = self.cbCycloneComPort.findText(cyclone_serial_port)
        if index >= 0:
            self.cbCycloneComPort.setCurrentIndex(index)
        else:
            index = self.cbCycloneComPort.findText('none')
            self.cbCycloneComPort.setCurrentIndex(index)

        modbus_serial_port = fl.configfileRead('MODBUS', 'COM_PORT')
        index = self.cbModbusComPort.findText(modbus_serial_port)
        if index >= 0:
            self.cbModbusComPort.setCurrentIndex(index)
        else:
            index = self.cbModbusComPort.findText('none')
            self.cbModbusComPort.setCurrentIndex(index)

        demojm_serial_port = fl.configfileRead('DEMOJM', 'COM_PORT')
        index = self.cbDemoJMComPort.findText(demojm_serial_port)
        if index >= 0:
            self.cbDemoJMComPort.setCurrentIndex(index)
        else:
            index = self.cbDemoJMComPort.findText('none')
            self.cbDemoJMComPort.setCurrentIndex(index)


def main():
    # a new app instance

    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
