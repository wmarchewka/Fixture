import threading
import time
import serial
try:
    import RPi.GPIO as gp
except ImportError:
    import FakeRPi.GPIO as gp
from PyQt5.QtWidgets import *
from QT_Project import mainwindow_auto as mw
from QT_Project import popupSlot_auto as pw
from QT_Project import popupModbus_auto as pmb
from PyQt5.QtCore import pyqtSignal
import SerialBarCodeModbusLibrary as ml
import ProgrammersLibrary as pl
import EthernetCommLibrary as el
import FileConfigurationLibrary as fl
import SupportLibrary as sl
import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog

global tfp3_serial_port
global scanner_serial_port
global cyclone_serial_port
global modbus_serial_port
global DemoJM_Serialport
global demojm_serial_port
global Testing
global serial_ports_descriptions
global serial_ports_list

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
# ****************************************************************************************************
class FileDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Browse for file....'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog()
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName
            logger.debug(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            logger.debug(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            logger.debug(fileName)

# ****************************************************************************************************
class popupModbus(QMainWindow, pmb.Ui_MainWindow):

    mbSendButton = pyqtSignal('int')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.title = 'Modbus read...'
        self.left = 200
        self.top = 200
        self.width = 200
        self.height = 100
        self.index = 0
        self.indexstr = ''
        self.initUI()

    def initUI(self):
        self.cmbMBRegisterType.addItem('Integer')
        self.cmbMBRegisterType.addItem('Float')
        self.cmbMBRegisterType.addItem('Text')
        self.cmbMBRegisterType.setCurrentIndex(1)
        self.cmbMBRegisterType.setCurrentIndex(2)
        self.txtMBValueToWrite.setText("")
        self.chkWrite.setChecked(False)
        self.txtMBNumberRegisters.setText('3')
        self.txtMBRegister.setText('345')
        self.txtMBUnitAddress.setText('1')
# ****************************************************************************************************
class popupCombo(QMainWindow, pw.Ui_MainWindow):

    changedValue = pyqtSignal('QString')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.title = 'Please select file type...'
        self.left = 200
        self.top = 200
        self.width = 200
        self.height = 100
        self.index = 0
        self.indexstr = ''
        self.initUI()

    def initUI(self):
        self.comboBox.addItem('wifi')
        self.comboBox.addItem('meter')
        self.comboBox.addItem('web')
        self.comboBox.addItem('firmware')
        self.comboBox.setCurrentIndex(1)
        self.comboBox.setCurrentIndex(0)

    def closeEvent(self, *args, **kwargs):
        pass

    # ****************************************************************************************************
class MainWindow(QMainWindow, mw.Ui_MainWindow):
    global DemoJM_Serialport
    serialtrigger = pyqtSignal(bytes)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file

        # setup serial triiger
        self.serialtrigger.connect(self.parse_serial_data)

        # setup button signals
        self.enable_disable_all_buttons('disconnect')

        # setup serial test input change signals
        self.lnSerialTest.textChanged.connect(self.SerialTest)

        # look to ensure we have a configuration file
        self.check_for_config()  # open configuration file

        # do all initializtion
        self.lblStatus.setText('')
        #self.populate_defaults()

        logger.debug('TFP3 relay pin ' + str(sl.supportLibrary.gpio_tfp3relay_pin))

        # check serial event thread
        #self.check_serial_event()

# ****************************************************************************************************
    def configure_logging():
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


# ****************************************************************************************************
    def enable_disable_all_buttons(self, state):


        if state == 'connect':
            self.pbPowerOn.clicked.connect(self.power_up_relay)
            self.pbPowerOff.clicked.connect(self.power_down_relay)
            self.pbButtonTest.clicked.connect(self.button_buttontest)
            self.pbTelnetGetVoltages.clicked.connect(self.button_voltages)
            self.pbReadScanner.clicked.connect(self.button_scanner)
            self.pbDoPing.clicked.connect(self.button_ping)
            self.pbProgCyclone.clicked.connect(self.button_cyclone)
            self.pbProgTFP3.clicked.connect(self.button_tfp3)
            self.pbResetTest.clicked.connect(self.button_reset)
            self.pbRebootUnit.clicked.connect(self.button_rebootunit)
            self.pbWriteLanMac.clicked.connect(self.button_lanmac)
            self.pbWriteWifiMac.clicked.connect(self.button_wifimac)
            self.pbManualWifiMac.clicked.connect(self.button_wifimanualmac)
            self.pbModbusInit.clicked.connect(self.button_modbusinit)
            self.pbModbusRead.clicked.connect(self.button_modbusread)
            self.pbDefaultsStore.clicked.connect(self.button_defaultsstore)
            self.pbSetPCR.clicked.connect(self.button_setpcr)
            self.pbWriteSerialNumber.clicked.connect(self.button_serialnumberwrite)
            self.pbUploadFile.clicked.connect(self.button_uploadfile)
            self.pbWriteScript.clicked.connect(self.button_scriptwrite)
            self.pbWifiVersion.clicked.connect(self.button_wifiversion)
            self.pbWebpageVersion.clicked.connect(self.button_webpageversion)
            self.pbSetupWIFI.clicked.connect(self.button_wifisetup)
            self.pbRescanSerialPorts.clicked.connect(self.button_populatedefaults)

        if state == 'disconnect':
            self.pbPowerOn.disconnect()
            self.pbPowerOff.disconnect()
            self.pbButtonTest.disconnect()
            self.pbTelnetGetVoltages.disconnect()
            self.pbReadScanner.disconnect()
            self.pbDoPing.disconnect()
            self.pbProgCyclone.disconnect()
            self.pbProgTFP3.disconnect()
            self.pbResetTest.disconnect()
            self.pbRebootUnit.disconnect()
            self.pbWriteLanMac.disconnect()
            self.pbWriteWifiMac.disconnect()
            self.pbManualWifiMac.disconnect()
            self.pbModbusInit.disconnect()
            self.pbModbusRead.disconnect()
            self.pbDefaultsStore.disconnect()
            self.pbSetPCR.disconnect()
            self.pbWriteSerialNumber.disconnect()
            self.pbUploadFile.disconnect()
            self.pbWriteScript.disconnect()
            self.pbWifiVersion.disconnect()
            self.pbWebpageVersion.disconnect()
            self.pbSetupWIFI.disconnect()
            self.pbRescanSerialPorts.disconnect()
    # ****************************************************************************************************
    def check_serial_event(self):
        logger.debug('Starting serial receive thread')
        self.lblStatus.setText('Starting serial receive thread')
        global DemoJM_Serialport
        DemoJM_Serialport = fl.configfileRead('DEMOJM','com_port')
        serial_thread = threading.Timer(1, self.check_serial_event)
        try:
            if DemoJM_Serialport.isOpen():
                serial_thread.start()
                logger.debug('Running serial thread')
                assert isinstance(DemoJM_Serialport, serial.Serial)
                if DemoJM_Serialport.inWaiting():
                    while True:
                        c = DemoJM_Serialport.read(1)
                        logger.debug('received ' + str(c))
                        if c:
                            self.serialtrigger.emit(c)
                            break
                        else:
                            break
        except OSError as err:
            logger.debug('Serial thread not running due to ' + str(err))
        except ValueError as err:
            logger.debug('Serial thread not running due to ' + str(err))
        except SystemError as err:
            logger.debug('Serial thread not running due to ' + str(err))
        except NameError as err:
            logger.debug('Serial thread not running due to ' + str(err))

    # ****************************************************************************************************
    def check_for_config(self):
        ret = fl.configfileRead('CONFIG', 'file_ver')
        #logger.debug('Found Configuration file version ' + ret)
        self.lblStatus.setText('Found Configuration file version ' + ret)

    # ****************************************************************************************************
    def limitswitch_check(self):
        logger.debug('limitswitch check')
        self.lblStatus.setText('limitswitch check')

    # ****************************************************************************************************
    def power_up_relay(self):
        logger.debug('power up power relay')
        self.lblStatus.setText('power up power relay')
        gp.output(sl.supportLibrary.gpio_powerrelay, sl.supportLibrary.gpio_on)

    # ****************************************************************************************************
    def power_cycle_relay(self):
        logger.debug('power cycle relay')
        self.lblStatus.setText('power cycle relay')
        gp.output(sl.supportLibrary.gpio_powerrelay, sl.supportLibrary.gpio_off)  ## Switch on pin 7
        time.sleep(2)
        gp.output(sl.supportLibrary.gpio_powerrelay, sl.supportLibrary.gpio_on)  ## Switch on pin 7

    # ****************************************************************************************************
    def power_down_relay(self):
        logger.debug('power down power relay')
        self.lblStatus.setText('power down power relay')
        gp.output(sl.supportLibrary.gpio_powerrelay, sl.supportLibrary.gpio_off)

    # ****************************************************************************************************
    def reset_tfp2(self):
        pass

    # ****************************************************************************************************
    def powerup_tfp3(self):
        logger.debug('power up tfp3 relay')
        self.lblStatus.setText('power up tfp3 relay')
        gp.output(sl.supportLibrary.gpio_tfp3relay_pin, sl.supportLibrary.gpio_on)

    # ****************************************************************************************************
    def powerdown_tfp3(self):
        logger.debug('power down tfp3 relay')
        self.lblStatus.setText('power down power relay')
        gp.output(sl.supportLibrary.gpio_tfp3relay_pin, sl.supportLibrary.gpio_off)

    # ****************************************************************************************************
    def adc(self):
        # TODO figure out what pin is the adc
        pass

    # ****************************************************************************************************
    def all_outputs_toggle(self):
        pass

    # ****************************************************************************************************
    def get_status(self):
        logger.debug('gpio get status off all pins')
        self.lblStatus.setText('gpio get status off all pins')

    # ****************************************************************************************************
    def send_report(self):
        pass

    # ****************************************************************************************************
    def SerialTest(self):
        'used to simulate receiving commands from labview'
        data = self.lnSerialTest.text()
        logger.debug('serial test ' + data)
        self.lnSerialTest.clear()
        self.parse_serial_data(data.encode('utf-8'))

    # ****************************************************************************************************
    def parse_serial_data(self, bData):
        logger.debug(bData)
        strData = bData.decode('utf-8')
        global DemoJM_Serialport
        DemoJM_Serialport = fl.configfileRead('DEMOJM','com_port')
        DemoJM_Serialport.write(bData + b'\r')
        self.txtSerialData.appendPlainText(strData)
        logger.debug('incoming serial data->' + strData)
        self.lblStatus.setText('incoming serial data->' + strData)
        if (strData == 'S') or (strData == 's'):
            MainWindow.send_report(self)
        elif (strData == 'L') or (strData == 'l'):
            MainWindow.limitswitch_check(self)
        elif (strData == 'Z') or (strData == 'z'):
            MainWindow.getstatus(self)
        else:
            try:
                # Send ACK to LabVIEW
                DemoJM_Serialport.write(b'K')
                DemoJM_Serialport.write(b'\r')
            except:
                logger.debug('no serial port')
                self.lblStatus.setText('no serial port')

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
    def button_rebootunit(self):
        self.lblStatus.setText("Rebooting unit...")
        logger.debug("Rebooting unit...")
        gui_thread = threading.Thread(None, self.rebootunit_command)
        gui_thread.start()

    # ****************************************************************************************************
    def rebootunit_command(self):
        self.lblStatus.setText("Rebooting Unit...")
        time.sleep(1)
        ret = el.EthComLib.rebootunit_check(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_reset(self):
        self.lblStatus.setText("Reset test...")
        logger.debug("Reset test...")
        gui_thread = threading.Thread(None, self.reset_command)
        gui_thread.start()

    # ****************************************************************************************************
    def reset_command(self):
        self.lblStatus.setText("Reset test running... !")
        time.sleep(1)
        ret = el.EthComLib.reset_button_check(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_lanmac(self):
        self.lblStatus.setText("Setting LAN MAC...")
        logger.debug("Setting LAN MAC...")
        gui_thread = threading.Thread(None, self.lanmac_command)
        gui_thread.start()

    # ****************************************************************************************************
    def lanmac_command(self):
        time.sleep(1)
        ret = el.EthComLib.lan_mac_write(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_wifimanualmac(self):
        self.lblStatus.setText("Setting WIFI MAC...")
        logger.debug("Setting WIFI MAC...")
        gui_thread = threading.Thread(None, self.wifimac_command)
        gui_thread.start()

    # ****************************************************************************************************
    def wifimanualmac_command(self):
        time.sleep(1)
        auto_inc = False
        new_mac = '58:2f:42:26:20:98'
        ret = el.EthComLib.wifi_mac_write(self, ip_address, auto_inc, new_mac)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_wifimac(self):
        self.lblStatus.setText("Setting WIFI MAC...")
        logger.debug("Setting WIFI MAC...")
        gui_thread = threading.Thread(None, self.wifimac_command)
        gui_thread.start()

    # ****************************************************************************************************
    def wifimac_command(self):
        time.sleep(1)
        auto_inc = False
        new_mac = '58:2f:42:26:20:98'
        ret = el.EthComLib.wifi_mac_write(self, ip_address, auto_inc, new_mac)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
    # ****************************************************************************************************
    def button_modbusread(self):
        self.lblStatus.setText("Reading Modbus register...")
        logger.debug("Reading Modbus register...")
        #TODO need to finish popup window for modbus entry
        self.popupModbusWindow = popupModbus()
        self.mbPushButton_connection(self.popupModbusWindow.pbSendButton)
        self.popupModbusWindow.show()

    # ****************************************************************************************************
    def modbusread_command(self, address, num_of_regs, register, type, write, valuetowrite):
        time.sleep(1)
        #type = 3   #0 = int  1 = float 2 = ascii
        modbus_serial_port = fl.configfileRead('MODBUS','com_port')
        ret = ml.SCML.mbComm(self, modbus_serial_port, address, register, type, num_of_regs, write, valuetowrite)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
    # ****************************************************************************************************
    def button_modbusinit(self):
        self.lblStatus.setText("Setting Modbus init...")
        logger.debug("Setting Modbus init...")
        gui_thread = threading.Thread(None, self.modbusinit_command)
        gui_thread.start()

    # ****************************************************************************************************
    def modbusinit_command(self):
        time.sleep(1)
        ret = el.EthComLib.modbus_init(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_defaultsstore(self):
        self.lblStatus.setText("Storing defaults...")
        time.sleep(1)
        logger.debug('Storing defaults...')
        gui_thread = threading.Thread(None, self.defaultsstore_command)
        gui_thread.start()

    # ****************************************************************************************************
    def defaultsstore_command(self):

        ret = el.EthComLib.defaults_store(self, ip_address)
        logger.debug(ret)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_setpcr(self):
        self.lblStatus.setText("Setting PCR...")
        logger.debug("Setting PCR...")
        gui_thread = threading.Thread(None, self.setpcr_command)
        gui_thread.start()

    # ****************************************************************************************************
    def setpcr_command(self):
        time.sleep(1)
        ret = el.EthComLib.pcr_write(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_serialnumberwrite(self):
        self.lblStatus.setText("Setting device serial number...")
        logger.debug("Setting device serial number...")
        oldserialnumber = self.readserialnumber_command()
        if oldserialnumber[0]:
            serialnumber, okPressed = QInputDialog.getText(self, 'Serial Number Entry', 'Old Serial Number -> ' + str(oldserialnumber[1]),QLineEdit.Normal)
            if okPressed:
                logger.debug(serialnumber)
                gui_thread = threading.Thread(None, self.writeserialnumber_command(ip_address, serialnumber))
                gui_thread.start()
            else:
                self.lblStatus.setText("Setting device serial number canceled. ..")
                logger.debug("Setting device serial number canceled. ..")
                #self.error_display_popup('Error Title','Error Message')

    # ****************************************************************************************************
    def writeserialnumber_command(self, ip_address, serialnumber):
        ret = el.EthComLib.serialnumber_write(self, ip_address, serialnumber)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned status ' + str(ret[0]))

    # ****************************************************************************************************
    def readserialnumber_command(self):
        ret = el.EthComLib.serialnumber_read(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
        return ret

    # ****************************************************************************************************
    def button_uploadfile(self):
        self.popupWindow = popupCombo()
        self.make_connection(self.popupWindow.comboBox)
        self.lblStatus.setText('Uploading file...')
        self.popupWindow.show()

   # ****************************************************************************************************
    def mbPushButton_connection(self, button_object):
        # TODO need to finish popup window for mobus
        button_object.clicked.connect(self.mbSendButton_Interim)
        pass
    # ****************************************************************************************************
    def make_connection(self, popup_combo_object):
        popup_combo_object.activated[str].connect(self.upload_file_interim)
        popup_combo_object

    # ****************************************************************************************************
    def mbSendButton_Interim(self, button_object):
        numreg = int(self.popupModbusWindow.txtMBNumberRegisters.toPlainText())
        reg = int(self.popupModbusWindow.txtMBRegister.toPlainText())
        addr = int(self.popupModbusWindow.txtMBUnitAddress.toPlainText())
        type = int(self.popupModbusWindow.cmbMBRegisterType.currentIndex())
        write = self.popupModbusWindow.chkWrite.isChecked()
        valuetowrite = self.popupModbusWindow.txtMBValueToWrite.toPlainText()
        self.popupModbusWindow.close()
        gui_thread = threading.Thread(None, self.modbusread_command(addr, numreg, reg, type, write, valuetowrite))
        gui_thread.start()

    # ****************************************************************************************************
    def upload_file_interim(self, slot):
        self.popupWindow.close()
        logger.debug("Uploading to slot " + str(slot))
        self.lblStatus.setText('Uploading to slot ' + str(slot) )
        gui_thread = threading.Thread(None, self.uploadfile_command, kwargs={'slot':slot})
        gui_thread.start()

    # ****************************************************************************************************
    def uploadfile_command(self, slot):
        self.lblStatus.setText('Uploading ' + str(slot))
        logger.debug('Upload ' + str(slot))
        ret = el.EthComLib.fileupload(self, ip_address, slot)
        #ret = el.EthComLib.waittest(self)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText('Returned Value ' + str(ret[1]))

    # ****************************************************************************************************
    def button_scriptwrite(self):
        #TODO: crashehes if file is not selected
        path = FileDialog.openFileNameDialog(self)
        logger.debug('filename ' + str(path))
        if path is not None:
            gui_thread = threading.Thread(None, self.scriptwrite_command(path))
            gui_thread.start()

    # ****************************************************************************************************
    def scriptwrite_command(self, path):
        time.sleep(1)
        self.lblStatus.setText("Writing script settings...")
        ip_address = '192.168.1.99'
        #path = r'C:\UEC\Functional Test\M50\Test_script.txt'
        ret = el.EthComLib.script_write(self, ip_address, path)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))
        return
    # ****************************************************************************************************
    def button_webpageversion(self):
        self.lblStatus.setText("Getting Webpage version...")
        time.sleep(1)
        logger.debug("Getting Webpage version...")
        gui_thread = threading.Thread(None, self.webpageversion_command)
        gui_thread.start()

    # ****************************************************************************************************
    def webpageversion_command(self):
        #ret = el.EthComLib.waittest(self)
        ret = el.EthComLib.webpageversion_read(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_wifiversion(self):
        self.lblStatus.setText("Getting WIFI version...")
        time.sleep(1)
        logger.debug("Getting WIFI version...")
        gui_thread = threading.Thread(None, self.wifiversion_command)
        gui_thread.start()

    # ****************************************************************************************************
    def wifiversion_command(self):
        #ret = el.EthComLib.waittest(self)
        ret = el.EthComLib.wifiversion_read(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_wifisetup(self):
        self.lblStatus.setText("Setting up WIFI...")
        time.sleep(1)
        logger.debug("Setting up WIFI...")
        gui_thread = threading.Thread(None, self.wifisetup_command)
        gui_thread.start()
    # ****************************************************************************************************
    def wifisetup_command(self):
        ret = el.EthComLib.wifi_setup(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_voltages(self):
        global ip_address
        logger.debug("Pressed voltage...")
        gui_thread = threading.Thread(None, self.voltages_command)
        gui_thread.start()

    # ****************************************************************************************************
    def voltages_command(self):
        self.lblStatus.setText("Getting voltages...")
        ret = el.EthComLib.voltage_read(self, ip_address)
        logger.debug(str(ret[1]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_tfp3(self):
        global tfp3_serial_port
        self.lblStatus.setText("TFP3 programming...")
        logger.debug('Starting TFP3 programmer on port ' + tfp3_serial_port)
        gui_thread = threading.Thread(None, self.tftp3_command)
        gui_thread.start()


    # ****************************************************************************************************
    def tftp3_command(self):
        self.lblStatus.setText("Programming TFP3 !")
        tfp3_serial_port = fl.configfileRead('TFP3','com_port')
        ret = pl.TFP3Program(self, tfp3_serial_port)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_cyclone(self):
        logger.debug("Programming cyclone !")
        gui_thread = threading.Thread(None, self.cyclone_command)
        gui_thread.start()

    # ****************************************************************************************************
    def cyclone_command(self):
        self.lblStatus.setText("Programming cyclone !")
        cyclone_serial_port = fl.configfileRead('CYCLONE','com_port')
        image = 3
        ret = pl.CycloneProgram(self, cyclone_serial_port, image)
        logger.debug('Returned value ' + str(ret[1]))
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_scanner(self):
        logger.debug("Pressed Scanner button...")
        gui_thread = threading.Thread(None, self.scanner_command, None)
        gui_thread.start()

    # ****************************************************************************************************
    def scanner_command(self):
        simulate = False
        scanner_serial_port = fl.configfileRead("SCANNER", 'com_port')
        ret = ml.SCML.ScanBarcode(self, simulate, scanner_serial_port, 5)
        logger.debug('Returned value ' + str(ret[0]))
        self.lblStatus.setText(str(ret[1]))


    # ****************************************************************************************************
    def button_buttontest(self):
        logger.debug("Pressed button test button")
        gui_thread = threading.Thread(None, self.buttonttest_command, None)
        gui_thread.start()

    # ****************************************************************************************************
    def buttonttest_command(self):
        self.lblStatus.setText("Button test running...")
        ret = el.EthComLib.m40_buttontest(self, ip_address)
        logger.debug('Returned value ' + str(ret[1]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_ping(self):
        logger.debug('Pressed ping button')
        gui_thread = threading.Thread(None, self.ping_command)
        gui_thread.start()

    # ****************************************************************************************************
    def ping_command(self):
        self.lblStatus.setText("Ping test running...")
        ret = el.EthComLib.pinguut(self, ip_address, 5)
        logger.debug('Returned value ' + str(ret[1]))
        self.lblStatus.setText(str(ret[1]))

    # ****************************************************************************************************
    def button_populatedefaults(self):
        logger.debug('Pressed repopulate serial ports')

        self.cbTFP3ComPort.currentIndexChanged.disconnect(self.tfp3SerialPortChanged)
        self.cbScannerComPort.currentIndexChanged.disconnect(self.ScannerSerialPortChanged)
        self.cbCycloneComPort.currentIndexChanged.disconnect(self.CycloneSerialPortChanged)
        self.cbModbusComPort.currentIndexChanged.disconnect(self.ModbusSerialPortChanged)
        self.cbDemoJMComPort.currentIndexChanged.disconnect(self.DemoJMSerialPortChanged)
        self.cbDemoJMComPort.activated[str].disconnect(self.DemoJMSerialPortChanged)

        self.cbTFP3ComPort.clear()
        self.cbScannerComPort.clear()
        self.cbCycloneComPort.clear()
        self.cbModbusComPort.clear()
        self.cbDemoJMComPort.clear()

        gui_thread = threading.Thread(None, self.populate_defaults)
        gui_thread.start()

    # ****************************************************************************************************
    def tfp3SerialPortChanged(self):
        global tfp3_serial_port
        logger.debug('TFP3 serial port changed....')
        tfp3_serial_port = self.cbTFP3ComPort.currentText()
        index = self.cbTFP3ComPort.currentIndex()
        port = serial_ports_list[index]
        fl.configfileWrite('TFP3', 'COM_DESCRIPTION', tfp3_serial_port)
        fl.configfileWrite('TFP3', 'COM_PORT', port)
        logger.debug('TFP3 port changed to  ' + tfp3_serial_port)

    # ****************************************************************************************************
    def ScannerSerialPortChanged(self):
        global scanner_serial_port
        logger.debug('Scanner serial port changed....')
        scanner_serial_port = self.cbScannerComPort.currentText()
        index = self.cbScannerComPort.currentIndex()
        port = serial_ports_list[index]
        fl.configfileWrite('SCANNER', 'COM_DESCRIPTION', scanner_serial_port)
        fl.configfileWrite('SCANNER', 'COM_PORT', port)
        logger.debug('Scanner port changed to ' + scanner_serial_port)

    # ****************************************************************************************************
    def CycloneSerialPortChanged(self):
        global cyclone_serial_port
        logger.debug('Cyclone serial port changed....')
        cyclone_serial_port = self.cbCycloneComPort.currentText()
        index = self.cbCycloneComPort.currentIndex()
        port = serial_ports_list[index]
        fl.configfileWrite('CYCLONE', 'COM_DESCRIPTION', cyclone_serial_port)
        fl.configfileWrite('CYCLONE', 'COM_PORT',  port)
        logger.debug('Cyclone port changed to ' + cyclone_serial_port)

    # ****************************************************************************************************
    def ModbusSerialPortChanged(self):
        global modbus_serial_port
        logger.debug('Modbus serial port changed....')
        modbus_serial_port = self.cbModbusComPort.currentText()
        index = self.cbModbusComPort.currentIndex()
        port = serial_ports_list[index]
        fl.configfileWrite('MODBUS', 'COM_DESCRIPTION', modbus_serial_port)
        fl.configfileWrite('MODBUS', 'COM_PORT', port)
        logger.debug('Modbus port changed to ' + modbus_serial_port)

    # ****************************************************************************************************
    def DemoJMSerialPortChanged(self):
        global demojm_serial_port
        logger.debug('DEMOJM serial port changed....')
        demojm_serial_port = self.cbDemoJMComPort.currentText()
        index = self.DemoJM_Serialport.currentIndex()
        port = serial_ports_list[index]
        fl.configfileWrite('DEMOJM', 'COM_DESCRIPTION', demojm_serial_port)
        fl.configfileWrite('DEMOJM', 'COM_PORT', port)
        logger.debug('DemoJM port changed to ' + demojm_serial_port)
        global DemoJM_Serialport
        try:
            demojm_serial_port = fl.configfileRead('DEMOJM', 'com_port')
            DemoJM_Serialport = serial.Serial(demojm_serial_port, baudrate=115200, timeout=10,
                                              parity=serial.PARITY_NONE,
                                              stopbits=serial.STOPBITS_ONE,
                                              bytesize=serial.EIGHTBITS
                                              )
            logger.debug('Opened demojm serial port on port ' + demojm_serial_port)
            #TODO reenable this
            #self.check_serial_event()

        except OSError as err:
            logger.debug(err)
        except ValueError as err:
            logger.debug(err)
        except SystemError as err:
            logger.debug(err)
        except NameError as err:
            logger.debug(err)

    # ****************************************************************************************************
    def collectserialports_command(self):
        global tfp3_serial_port
        global scanner_serial_port
        global cyclone_serial_port
        global modbus_serial_port
        global demojm_serial_port
        global DemoJM_Serialport
        global serial_ports_descriptions
        global serial_ports_list

        self.lblStatus.setText("Searching for serial ports...")
        logger.debug("Searching for serial ports...")

        time.sleep(1)
        # read serial port list OS and populate comboboxes
        ret = ml.SCML.collectSerialPorts(self)  # run serial port routine

        if ret[0] is True:
            logger.debug('List->' + str(ret[1]))
            logger.debug('modbus port->' + str(ret[3]))
            logger.debug('modbus port description->' + str(ret[4]))
            logger.debug('tfp3 port->' + str(ret[5]))
            logger.debug('tfp3 port description->' + str(ret[6]))
            logger.debug('scanner port->' + str(ret[7]))
            logger.debug('scanner port description->' + str(ret[8]))
            logger.debug('cyclone port' + str(ret[9]))
            logger.debug('cyclone port description' + str(ret[10]))
            logger.debug('demojm port' + str(ret[11]))
            logger.debug('demojm port description' + str(ret[12]))

            if ret[1]:
                serial_ports_list = ret[1]
                logger.debug('ports->' + str(serial_ports_list))
                serial_ports_descriptions = ret[2]
                logger.debug('description->' + str(serial_ports_descriptions))

            self.cbTFP3ComPort.addItems(serial_ports_descriptions)
            self.cbScannerComPort.addItems(serial_ports_descriptions)
            self.cbCycloneComPort.addItems(serial_ports_descriptions)
            self.cbModbusComPort.addItems(serial_ports_descriptions)
            self.cbDemoJMComPort.addItems(serial_ports_descriptions)
        else:
            logger.debug('Error getting serial port list')
            self.lblStatus.setText('Error getting serial port list')
            time.sleep(2)

    # ****************************************************************************************************
    def populate_defaults(self):

        global tfp3_serial_port
        global scanner_serial_port
        global cyclone_serial_port
        global modbus_serial_port
        global demojm_serial_port
        global DemoJM_Serialport

        logger.debug('Populating defaults...')
        self.lblStatus.setText("Searching for serial ports...")
        time.sleep(1)

        self.collectserialports_command()

        global ip_address

        os_name = sl.supportLibrary.getOsPlatform(self)
        logger.debug('os name->' + os_name)

        ip_address = fl.configfileRead('TELNET', 'ip_address')

        tfp3_serial_port = fl.configfileRead('TFP3', 'COM_DESCRIPTION')
        index = self.cbTFP3ComPort.findText(tfp3_serial_port)
        if index >= 0:
            self.cbTFP3ComPort.setCurrentIndex(index)
        else:
            index = self.cbTFP3ComPort.findText('None')
            self.cbTFP3ComPort.setCurrentIndex(index)

        scanner_serial_port = fl.configfileRead('SCANNER', 'COM_DESCRIPTION')
        index = self.cbScannerComPort.findText(scanner_serial_port)
        if index >= 0:
            self.cbScannerComPort.setCurrentIndex(index)
        else:
            index = self.cbScannerComPort.findText('None')
            self.cbScannerComPort.setCurrentIndex(index)

        cyclone_serial_port = fl.configfileRead('CYCLONE', 'COM_DESCRIPTION')
        index = self.cbCycloneComPort.findText(cyclone_serial_port)
        if index >= 0:
            self.cbCycloneComPort.setCurrentIndex(index)
        else:
            index = self.cbCycloneComPort.findText('None')
            self.cbCycloneComPort.setCurrentIndex(index)

        modbus_serial_port = fl.configfileRead('MODBUS', 'COM_DESCRIPTION')
        index = self.cbModbusComPort.findText(modbus_serial_port)
        if index >= 0:
            self.cbModbusComPort.setCurrentIndex(index)
        else:
            index = self.cbModbusComPort.findText('None')
            self.cbModbusComPort.setCurrentIndex(index)

        demojm_serial_port = fl.configfileRead('DEMOJM', 'COM_DESCRIPTION')
        index = self.cbDemoJMComPort.findText(demojm_serial_port)
        if index >= 0:
            self.cbDemoJMComPort.setCurrentIndex(index)
        else:
            index = self.cbDemoJMComPort.findText('None')
            self.cbDemoJMComPort.setCurrentIndex(index)

        # setup combobox change signals
        self.cbTFP3ComPort.currentIndexChanged.connect(self.tfp3SerialPortChanged)
        self.cbScannerComPort.currentIndexChanged.connect(self.ScannerSerialPortChanged)
        self.cbCycloneComPort.currentIndexChanged.connect(self.CycloneSerialPortChanged)
        self.cbModbusComPort.currentIndexChanged.connect(self.ModbusSerialPortChanged)
        self.cbDemoJMComPort.currentIndexChanged.connect(self.DemoJMSerialPortChanged)
        self.cbDemoJMComPort.activated[str].connect(self.DemoJMSerialPortChanged)

        self.enable_disable_all_buttons('connect')

        self.lblStatus.setText('Ready...')

    # ****************************************************************************************************
    def error_display_popup(self, title, message):
        logger.debug('error display')
        buttonReply = QMessageBox.question(self, title, message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            logger.debug('Yes clicked.')
        else:
            logger.debug('No clicked.')

# ****************************************************************************************************
def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    gui_thread = threading.Thread(None,form.populate_defaults)
    gui_thread.start()
    form.lblStatus.setText('Ready...')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
