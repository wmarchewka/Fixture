# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pbPowerOn = QtWidgets.QPushButton(self.centralWidget)
        self.pbPowerOn.setGeometry(QtCore.QRect(10, 200, 130, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbPowerOn.setFont(font)
        self.pbPowerOn.setObjectName("pbPowerOn")
        self.pbPowerOff = QtWidgets.QPushButton(self.centralWidget)
        self.pbPowerOff.setGeometry(QtCore.QRect(10, 230, 130, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbPowerOff.setFont(font)
        self.pbPowerOff.setObjectName("pbPowerOff")
        self.cbTFP3ComPort = QtWidgets.QComboBox(self.centralWidget)
        self.cbTFP3ComPort.setGeometry(QtCore.QRect(140, 50, 251, 22))
        self.cbTFP3ComPort.setObjectName("cbTFP3ComPort")
        self.lblTFP3ComPort = QtWidgets.QLabel(self.centralWidget)
        self.lblTFP3ComPort.setGeometry(QtCore.QRect(30, 50, 101, 16))
        self.lblTFP3ComPort.setObjectName("lblTFP3ComPort")
        self.lblCycloneComPort = QtWidgets.QLabel(self.centralWidget)
        self.lblCycloneComPort.setGeometry(QtCore.QRect(10, 80, 121, 16))
        self.lblCycloneComPort.setObjectName("lblCycloneComPort")
        self.cbCycloneComPort = QtWidgets.QComboBox(self.centralWidget)
        self.cbCycloneComPort.setGeometry(QtCore.QRect(140, 80, 251, 22))
        self.cbCycloneComPort.setObjectName("cbCycloneComPort")
        self.cbScannerComPort = QtWidgets.QComboBox(self.centralWidget)
        self.cbScannerComPort.setGeometry(QtCore.QRect(140, 110, 251, 22))
        self.cbScannerComPort.setObjectName("cbScannerComPort")
        self.lblScannerComPort = QtWidgets.QLabel(self.centralWidget)
        self.lblScannerComPort.setGeometry(QtCore.QRect(10, 110, 131, 16))
        self.lblScannerComPort.setObjectName("lblScannerComPort")
        self.lblModbusComPort = QtWidgets.QLabel(self.centralWidget)
        self.lblModbusComPort.setGeometry(QtCore.QRect(20, 20, 111, 20))
        self.lblModbusComPort.setObjectName("lblModbusComPort")
        self.cbModbusComPort = QtWidgets.QComboBox(self.centralWidget)
        self.cbModbusComPort.setGeometry(QtCore.QRect(140, 20, 251, 22))
        self.cbModbusComPort.setObjectName("cbModbusComPort")
        self.pbProgTFP3 = QtWidgets.QPushButton(self.centralWidget)
        self.pbProgTFP3.setGeometry(QtCore.QRect(150, 200, 130, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbProgTFP3.setFont(font)
        self.pbProgTFP3.setObjectName("pbProgTFP3")
        self.pbProgCyclone = QtWidgets.QPushButton(self.centralWidget)
        self.pbProgCyclone.setGeometry(QtCore.QRect(150, 230, 130, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbProgCyclone.setFont(font)
        self.pbProgCyclone.setObjectName("pbProgCyclone")
        self.pbReadScanner = QtWidgets.QPushButton(self.centralWidget)
        self.pbReadScanner.setGeometry(QtCore.QRect(290, 200, 130, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbReadScanner.setFont(font)
        self.pbReadScanner.setObjectName("pbReadScanner")
        self.pbButtonTest = QtWidgets.QPushButton(self.centralWidget)
        self.pbButtonTest.setGeometry(QtCore.QRect(430, 200, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbButtonTest.setFont(font)
        self.pbButtonTest.setObjectName("pbButtonTest")
        self.pbDoPing = QtWidgets.QPushButton(self.centralWidget)
        self.pbDoPing.setGeometry(QtCore.QRect(430, 230, 130, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbDoPing.setFont(font)
        self.pbDoPing.setObjectName("pbDoPing")
        self.pbGetADC = QtWidgets.QPushButton(self.centralWidget)
        self.pbGetADC.setGeometry(QtCore.QRect(290, 230, 130, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbGetADC.setFont(font)
        self.pbGetADC.setObjectName("pbGetADC")
        self.pbRescanSerialPorts = QtWidgets.QPushButton(self.centralWidget)
        self.pbRescanSerialPorts.setGeometry(QtCore.QRect(420, 60, 161, 23))
        self.pbRescanSerialPorts.setObjectName("pbRescanSerialPorts")
        self.lblStatus = QtWidgets.QLabel(self.centralWidget)
        self.lblStatus.setGeometry(QtCore.QRect(130, 390, 351, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblStatus.setFont(font)
        self.lblStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.lblStatus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lblStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lblStatus.setWordWrap(True)
        self.lblStatus.setObjectName("lblStatus")
        self.cbDemoJMComPort = QtWidgets.QComboBox(self.centralWidget)
        self.cbDemoJMComPort.setGeometry(QtCore.QRect(140, 140, 251, 22))
        self.cbDemoJMComPort.setObjectName("cbDemoJMComPort")
        self.lblDemoJM = QtWidgets.QLabel(self.centralWidget)
        self.lblDemoJM.setGeometry(QtCore.QRect(10, 140, 131, 16))
        self.lblDemoJM.setObjectName("lblDemoJM")
        self.txtSerialData = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.txtSerialData.setGeometry(QtCore.QRect(630, 10, 111, 411))
        self.txtSerialData.setObjectName("txtSerialData")
        self.lnSerialTest = QtWidgets.QLineEdit(self.centralWidget)
        self.lnSerialTest.setGeometry(QtCore.QRect(630, 440, 113, 21))
        self.lnSerialTest.setObjectName("lnSerialTest")
        self.pbTelnetGetVoltages = QtWidgets.QPushButton(self.centralWidget)
        self.pbTelnetGetVoltages.setGeometry(QtCore.QRect(430, 260, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbTelnetGetVoltages.setFont(font)
        self.pbTelnetGetVoltages.setObjectName("pbTelnetGetVoltages")
        self.pbResetTest = QtWidgets.QPushButton(self.centralWidget)
        self.pbResetTest.setGeometry(QtCore.QRect(10, 260, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbResetTest.setFont(font)
        self.pbResetTest.setObjectName("pbResetTest")
        self.pbWriteLanMac = QtWidgets.QPushButton(self.centralWidget)
        self.pbWriteLanMac.setGeometry(QtCore.QRect(150, 260, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbWriteLanMac.setFont(font)
        self.pbWriteLanMac.setObjectName("pbWriteLanMac")
        self.pbWriteWifiMac = QtWidgets.QPushButton(self.centralWidget)
        self.pbWriteWifiMac.setGeometry(QtCore.QRect(290, 260, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbWriteWifiMac.setFont(font)
        self.pbWriteWifiMac.setObjectName("pbWriteWifiMac")
        self.pbModbusInit = QtWidgets.QPushButton(self.centralWidget)
        self.pbModbusInit.setGeometry(QtCore.QRect(10, 290, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbModbusInit.setFont(font)
        self.pbModbusInit.setObjectName("pbModbusInit")
        self.pbSetPCR = QtWidgets.QPushButton(self.centralWidget)
        self.pbSetPCR.setGeometry(QtCore.QRect(150, 290, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbSetPCR.setFont(font)
        self.pbSetPCR.setObjectName("pbSetPCR")
        self.pbWriteSerialNumber = QtWidgets.QPushButton(self.centralWidget)
        self.pbWriteSerialNumber.setGeometry(QtCore.QRect(290, 290, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbWriteSerialNumber.setFont(font)
        self.pbWriteSerialNumber.setObjectName("pbWriteSerialNumber")
        self.pbUploadFile = QtWidgets.QPushButton(self.centralWidget)
        self.pbUploadFile.setGeometry(QtCore.QRect(430, 290, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbUploadFile.setFont(font)
        self.pbUploadFile.setObjectName("pbUploadFile")
        self.pbWriteScript = QtWidgets.QPushButton(self.centralWidget)
        self.pbWriteScript.setGeometry(QtCore.QRect(10, 320, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbWriteScript.setFont(font)
        self.pbWriteScript.setObjectName("pbWriteScript")
        self.pbWifiVersion = QtWidgets.QPushButton(self.centralWidget)
        self.pbWifiVersion.setGeometry(QtCore.QRect(150, 320, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbWifiVersion.setFont(font)
        self.pbWifiVersion.setObjectName("pbWifiVersion")
        self.pbSetupWIFI = QtWidgets.QPushButton(self.centralWidget)
        self.pbSetupWIFI.setGeometry(QtCore.QRect(290, 320, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbSetupWIFI.setFont(font)
        self.pbSetupWIFI.setObjectName("pbSetupWIFI")
        self.pbDefaultsStore = QtWidgets.QPushButton(self.centralWidget)
        self.pbDefaultsStore.setGeometry(QtCore.QRect(430, 320, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pbDefaultsStore.setFont(font)
        self.pbDefaultsStore.setObjectName("pbDefaultsStore")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fixture"))
        self.pbPowerOn.setText(_translate("MainWindow", "POWER ON"))
        self.pbPowerOff.setText(_translate("MainWindow", "POWER OFF"))
        self.lblTFP3ComPort.setText(_translate("MainWindow", "TFP3 Com Port"))
        self.lblCycloneComPort.setText(_translate("MainWindow", "Cyclone Com Port"))
        self.lblScannerComPort.setText(_translate("MainWindow", "Scanner Com Port"))
        self.lblModbusComPort.setText(_translate("MainWindow", "Modbus Com Port"))
        self.pbProgTFP3.setText(_translate("MainWindow", "PROG TFP3 "))
        self.pbProgCyclone.setText(_translate("MainWindow", "PROG CYCLONE"))
        self.pbReadScanner.setText(_translate("MainWindow", "READ SCANNER"))
        self.pbButtonTest.setText(_translate("MainWindow", "BUTTON TEST"))
        self.pbDoPing.setText(_translate("MainWindow", "PING TEST"))
        self.pbGetADC.setText(_translate("MainWindow", "GET ADC"))
        self.pbRescanSerialPorts.setText(_translate("MainWindow", "Re-scan serial ports"))
        self.lblStatus.setText(_translate("MainWindow", "TextLabel"))
        self.lblDemoJM.setText(_translate("MainWindow", "Demo JM"))
        self.pbTelnetGetVoltages.setText(_translate("MainWindow", "GET VOLTAGES"))
        self.pbResetTest.setText(_translate("MainWindow", "RESET TEST"))
        self.pbWriteLanMac.setText(_translate("MainWindow", "WRITE LAN MAC"))
        self.pbWriteWifiMac.setText(_translate("MainWindow", "WRITE WIFI MAC"))
        self.pbModbusInit.setText(_translate("MainWindow", "MODBUS INIT"))
        self.pbSetPCR.setText(_translate("MainWindow", "SET PCR"))
        self.pbWriteSerialNumber.setText(_translate("MainWindow", "SERIAL NUMBER"))
        self.pbUploadFile.setText(_translate("MainWindow", "UPLOAD FILE"))
        self.pbWriteScript.setText(_translate("MainWindow", "WRITE SCRIPT"))
        self.pbWifiVersion.setText(_translate("MainWindow", "WIFI VERSION"))
        self.pbSetupWIFI.setText(_translate("MainWindow", "SETUP WIFI"))
        self.pbDefaultsStore.setText(_translate("MainWindow", "STORE DEFAULTS"))

