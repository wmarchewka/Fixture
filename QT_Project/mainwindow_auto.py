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
        MainWindow.resize(768, 494)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pbPowerOn = QtWidgets.QPushButton(self.centralWidget)
        self.pbPowerOn.setGeometry(QtCore.QRect(10, 200, 130, 23))
        self.pbPowerOn.setObjectName("pbPowerOn")
        self.pbPowerOff = QtWidgets.QPushButton(self.centralWidget)
        self.pbPowerOff.setGeometry(QtCore.QRect(10, 230, 130, 23))
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
        self.pbProgTFP3.setObjectName("pbProgTFP3")
        self.pbProgCyclone = QtWidgets.QPushButton(self.centralWidget)
        self.pbProgCyclone.setGeometry(QtCore.QRect(150, 230, 130, 23))
        self.pbProgCyclone.setObjectName("pbProgCyclone")
        self.pbReadScanner = QtWidgets.QPushButton(self.centralWidget)
        self.pbReadScanner.setGeometry(QtCore.QRect(290, 200, 130, 23))
        self.pbReadScanner.setObjectName("pbReadScanner")
        self.pbSendTelnet = QtWidgets.QPushButton(self.centralWidget)
        self.pbSendTelnet.setGeometry(QtCore.QRect(430, 200, 131, 23))
        self.pbSendTelnet.setObjectName("pbSendTelnet")
        self.pbDoPing = QtWidgets.QPushButton(self.centralWidget)
        self.pbDoPing.setGeometry(QtCore.QRect(430, 230, 130, 23))
        self.pbDoPing.setObjectName("pbDoPing")
        self.pbGetADC = QtWidgets.QPushButton(self.centralWidget)
        self.pbGetADC.setGeometry(QtCore.QRect(290, 230, 130, 23))
        self.pbGetADC.setObjectName("pbGetADC")
        self.pbRescanSerialPorts = QtWidgets.QPushButton(self.centralWidget)
        self.pbRescanSerialPorts.setGeometry(QtCore.QRect(420, 60, 161, 23))
        self.pbRescanSerialPorts.setObjectName("pbRescanSerialPorts")
        self.lblStatus = QtWidgets.QLabel(self.centralWidget)
        self.lblStatus.setGeometry(QtCore.QRect(130, 320, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblStatus.setFont(font)
        self.lblStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.lblStatus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lblStatus.setAlignment(QtCore.Qt.AlignCenter)
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
        self.lnSerialTest.setGeometry(QtCore.QRect(480, 360, 113, 21))
        self.lnSerialTest.setObjectName("lnSerialTest")
        self.pbTelnetGetVoltages = QtWidgets.QPushButton(self.centralWidget)
        self.pbTelnetGetVoltages.setGeometry(QtCore.QRect(430, 260, 131, 23))
        self.pbTelnetGetVoltages.setObjectName("pbTelnetGetVoltages")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 768, 21))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pbPowerOn.setText(_translate("MainWindow", "POWER ON"))
        self.pbPowerOff.setText(_translate("MainWindow", "POWER OFF"))
        self.lblTFP3ComPort.setText(_translate("MainWindow", "TFP3 Com Port"))
        self.lblCycloneComPort.setText(_translate("MainWindow", "Cyclone Com Port"))
        self.lblScannerComPort.setText(_translate("MainWindow", "Scanner Com Port"))
        self.lblModbusComPort.setText(_translate("MainWindow", "Modbus Com Port"))
        self.pbProgTFP3.setText(_translate("MainWindow", "PROG TFP3 "))
        self.pbProgCyclone.setText(_translate("MainWindow", "PROG CYCLONE"))
        self.pbReadScanner.setText(_translate("MainWindow", "READ SCANNER"))
        self.pbSendTelnet.setText(_translate("MainWindow", "TELNET"))
        self.pbDoPing.setText(_translate("MainWindow", "Do PING"))
        self.pbGetADC.setText(_translate("MainWindow", "GET ADC"))
        self.pbRescanSerialPorts.setText(_translate("MainWindow", "Re-scan serial ports"))
        self.lblStatus.setText(_translate("MainWindow", "TextLabel"))
        self.lblDemoJM.setText(_translate("MainWindow", "Demo JM"))
        self.pbTelnetGetVoltages.setText(_translate("MainWindow", "GET VOLTAGES"))
