import GetOS as gos
os_name = gos.get_platform()
print('os name->' + os_name)
import RPi.GPIO as gp
import threading
import serial
import time
import TelnetGetVoltagesCurrents as gv
import TFP3_Program as tf
import Cyclone_Program as pc
import GetSerialPorts as gs
import BarCode as sc
import Configuration as cf
import mainwindow_auto
from PyQt5.QtCore import QObject, pyqtSignal
import GPIO_Init
from PyQt5.QtWidgets import *
import PingUUT as pn

global ser


class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow,GPIO_Init.Init):

    serialtrigger = pyqtSignal(str)


    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file

        self.serialtrigger.connect(self.parse_serial_data)


        serial_ports_list = gs.serial_ports()

        self.cbTFP3ComPort.addItems(serial_ports_list)
        self.cbScannerComPort.addItems(serial_ports_list)
        self.cbCycloneComPort.addItems(serial_ports_list)
        self.cbModbusComPort.addItems(serial_ports_list)
        self.cbDemoJMComPort.addItems(serial_ports_list)
        self.pbPowerOn.clicked.connect(lambda: self.power_up_relay())
        self.pbPowerOff.clicked.connect(lambda: self.power_down_relay())
        self.pbSendTelnet.clicked.connect(lambda: self.pressedTelnetButton())
        self.pbTelnetGetVoltages.clicked.connect(lambda: self.TelnetGetVoltage())
        self.pbReadScanner.clicked.connect(lambda: self.pressedSendScannerButton())
        self.pbDoPing.clicked.connect(lambda: self.PingUUT())
        self.pbProgCyclone.clicked.connect(lambda: self.programCyclone())
        self.pbProgTFP3.clicked.connect(lambda: self.pressedTFP3Button())
        self.cbTFP3ComPort.currentIndexChanged.connect(self.tfp3SerialPortChanged)
        self.cbScannerComPort.currentIndexChanged.connect(self.ScannerSerialPortChanged)
        self.cbCycloneComPort.currentIndexChanged.connect(self.CycloneSerialPortChanged)
        self.cbModbusComPort.currentIndexChanged.connect(self.ModbusSerialPortChanged)
        self.cbDemoJMComPort.currentIndexChanged.connect(self.DemoJMSerialPortChanged)
        self.lnSerialTest.textChanged.connect(self.SerialTest)

        self.populate_defaults()

        print(self.tfp3relay_pin)
        self.check_serial_event()

    def check_serial_event(self):
        serial_thread = threading.Timer(1, self.check_serial_event)
        try:
            if ser.is_open == True:
                serial_thread.start()
                print('running serial thread')
                while True:
                    #TODO need timeout here so doesnt block
                    #c = ser.read(1)
                    time.sleep(5)           #
                    c="P"
                    if c:
                        self.serialtrigger.emit(c)
                        break
                    else:
                        break
        except:
            print('serial port not found')
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

        pass


    def send_report(self):
        pass

    def SerialTest(self):
        data = self.lnSerialTest.text()
        print('serial test' + data)
        self.lnSerialTest.clear()
        self.parse_serial_data(data)

    def parse_serial_data(self,strData):

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
                ser.write(b'K')
                ser.write(b'\x0a')
                ser.write(b'\x0d')
            except:
                print('no serial port')

        if ((strData == 'P') or (strData == 'p')):
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
            MainWindow.all_outputs_toggle(self)

    def scanSerialPorts(self):
        serial_ports_list = gs.serial_ports()
        self.cbTFP3ComPort.addItems(serial_ports_list)
        self.cbScannerComPort.addItems(serial_ports_list)
        self.cbCycloneComPort.addItems(serial_ports_list)
        self.cbModbusComPort.addItems(serial_ports_list)
        self.populate_defaults()

    def TelnetGetVoltage(self):
        print("Pressed voltage...")
        data = gv.GetTelnetVoltages(self)
        OS_NAME = data
        print(data)

    def pressedSendSerialButton(self):
        print("Pressed Serial Send")

    def pressedTFP3Button(self):
        self.lblStatus.setText("TFP3 programming...")
        print('Starting TFP3 programmer on port ' + tfp3_serial_port)
        ret = tf.StartProgram(tfp3_serial_port)
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
        if ret[0]:
            pass
        else:
            pass

    def programCyclone(self):
        self.lblStatus.setText("Progrraming cyclone !")
        print("Programming cyclone !")
        ret = pc.Main.ProgramCyclone(cyclone_serial_port)
        print ('Returned value '+ str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
        if ret[0]:
            pass
        else:
            pass


    def pressedSendScannerButton(self):
        print("Pressed Scanner Send")
        ret = sc.ScanBarcode(scanner_serial_port)
        print('Received from scanner: '+ str(ret[0]))

        if ret:
            pass
        else:
            pass

    def pressedTelnetButton(self):
        print("Pressed Telnet")

    def PingUUT(self):
        ret = pn.PingUUT('192.168.1.99', 5)
        print('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
        if ret[0]:
            pass
        else:
            pass

    def tfp3SerialPortChanged(self):
        global tfp3_serial_port
        tfp3_serial_port = self.cbTFP3ComPort.currentText()
        cf.config_write('TFP3','COM_PORT',tfp3_serial_port)
        print('TFP3 port changed to  ' + tfp3_serial_port)

    def ScannerSerialPortChanged(self):
        global scanner_serial_port
        scanner_serial_port = self.cbScannerComPort.currentText()
        cf.config_write('SCANNER','COM_PORT',scanner_serial_port)
        print('Scanner port changed to '+ scanner_serial_port )

    def CycloneSerialPortChanged(self):
        global cyclone_serial_port
        cyclone_serial_port = self.cbCycloneComPort.currentText()
        cf.config_write('CYCLONE','COM_PORT',cyclone_serial_port)
        print('Cyclone port changed to ' + cyclone_serial_port)

    def ModbusSerialPortChanged(self):
        global modbus_serial_port
        modbus_serial_port = self.cbModbusComPort.currentText()
        cf.config_write('MODBUS','COM_PORT',modbus_serial_port)
        print('Modbus port changed to ' + modbus_serial_port)

    def DemoJMSerialPortChanged(self):
        global demojm_serial_port
        demojm_serial_port = self.cbDemoJMComPort.currentText()
        cf.config_write('DemoJM', 'COM_PORT', demojm_serial_port)
        print('DemoJM port changed to ' + demojm_serial_port)


    def populate_defaults(self):
        global tfp3_serial_port
        global scanner_serial_port
        global cyclone_serial_port
        global modbus_serial_port
        global demojm_serial_port

        tfp3_serial_port = cf.config_read('TFP3', 'COM_PORT')
        index = self.cbTFP3ComPort.findText(tfp3_serial_port)
        if index >= 0:
            self.cbTFP3ComPort.setCurrentIndex(index)

        scanner_serial_port = cf.config_read('SCANNER', 'COM_PORT')
        index = self.cbScannerComPort.findText(scanner_serial_port)
        if index >= 0:
            self.cbScannerComPort.setCurrentIndex(index)

        cyclone_serial_port = cf.config_read('CYCLONE', 'COM_PORT')
        index = self.cbCycloneComPort.findText(cyclone_serial_port)
        if index >= 0:
            self.cbCycloneComPort.setCurrentIndex(index)

        modbus_serial_port = cf.config_read('MODBUS', 'COM_PORT')
        index = self.cbModbusComPort.findText(modbus_serial_port)
        if index >= 0:
            self.cbModbusComPort.setCurrentIndex(index)

        demojm_serial_port = cf.config_read('DEMOJM', 'COM_PORT')
        index = self.cbDemoJMComPort.findText(demojm_serial_port)
        if index >= 0:
            self.cbDemoJMComPort.setCurrentIndex(index)
        try:
            ser = serial.Serial(demojm_serial_port, baudrate=115200, timeout=10,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS
                            )
        except:
            ser = None
            print('cannot find serial port')

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

