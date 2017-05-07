#native libraries
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
#my libraries
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
        self.serialtrigger.connect(self.parse_serial_data)
        serial_ports_list = ml.collectSerialPorts()  # run serial port routine
        self.cbTFP3ComPort.addItems(serial_ports_list)
        self.cbScannerComPort.addItems(serial_ports_list)
        self.cbCycloneComPort.addItems(serial_ports_list)
        self.cbModbusComPort.addItems(serial_ports_list)
        self.cbDemoJMComPort.addItems(serial_ports_list)
        self.pbPowerOn.clicked.connect(lambda: self.power_up_relay())
        self.pbPowerOff.clicked.connect(lambda: self.power_down_relay())
        self.pbSendTelnet.clicked.connect(lambda: self.pressedResetButton())
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

    def pressedResetButton(self):
        print("Pressed reset button")
        ret = el.EthComLib.check_reset_button(self,ip_address)


    def PingUUT(self):
        ret = el.EthComLib.pinguut(self, ip_address, 5)
        print('Returned value ' + str(ret[0]))


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
        os_name = sl.getOsPlatform()
        print('os name->' + os_name)
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

    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
