# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        self.inputText = QtWidgets.QTextEdit(Dialog)
        self.inputText.setGeometry(QtCore.QRect(10, 20, 291, 31))
        self.inputText.setObjectName("inputText")
        self.pkOK = QtWidgets.QPushButton(Dialog)
        self.pkOK.setGeometry(QtCore.QRect(210, 190, 75, 23))
        self.pkOK.setObjectName("pkOK")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pkOK.setText(_translate("Dialog", "PushButton"))

