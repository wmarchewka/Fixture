# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popupmodbus.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(343, 253)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.txtMBRegister = QtWidgets.QTextEdit(self.centralwidget)
        self.txtMBRegister.setGeometry(QtCore.QRect(20, 40, 91, 31))
        self.txtMBRegister.setObjectName("txtMBRegister")
        self.txtMBNumberRegisters = QtWidgets.QTextEdit(self.centralwidget)
        self.txtMBNumberRegisters.setGeometry(QtCore.QRect(130, 40, 91, 31))
        self.txtMBNumberRegisters.setObjectName("txtMBNumberRegisters")
        self.cmbMBRegisterType = QtWidgets.QComboBox(self.centralwidget)
        self.cmbMBRegisterType.setGeometry(QtCore.QRect(230, 40, 81, 31))
        self.cmbMBRegisterType.setObjectName("cmbMBRegisterType")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 20, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(240, 20, 71, 16))
        self.label_3.setObjectName("label_3")
        self.txtMBUnitAddress = QtWidgets.QTextEdit(self.centralwidget)
        self.txtMBUnitAddress.setGeometry(QtCore.QRect(20, 190, 91, 31))
        self.txtMBUnitAddress.setObjectName("txtMBUnitAddress")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 170, 71, 16))
        self.label_4.setObjectName("label_4")
        self.pbSendButton = QtWidgets.QPushButton(self.centralwidget)
        self.pbSendButton.setGeometry(QtCore.QRect(230, 190, 81, 31))
        self.pbSendButton.setObjectName("pbSendButton")
        self.chkWrite = QtWidgets.QCheckBox(self.centralwidget)
        self.chkWrite.setGeometry(QtCore.QRect(220, 120, 101, 20))
        self.chkWrite.setObjectName("chkWrite")
        self.txtMBValueToWrite = QtWidgets.QTextEdit(self.centralwidget)
        self.txtMBValueToWrite.setGeometry(QtCore.QRect(20, 110, 191, 31))
        self.txtMBValueToWrite.setObjectName("txtMBValueToWrite")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 90, 71, 16))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Start Register"))
        self.label_2.setText(_translate("MainWindow", "Number Registers"))
        self.label_3.setText(_translate("MainWindow", "Register Type"))
        self.label_4.setText(_translate("MainWindow", "Unit Address"))
        self.pbSendButton.setText(_translate("MainWindow", "SEND"))
        self.chkWrite.setText(_translate("MainWindow", "WRITE VALUES"))
        self.label_5.setText(_translate("MainWindow", "Value to write"))

