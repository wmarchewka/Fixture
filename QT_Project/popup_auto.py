# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 240)
        self.pbOK = QtWidgets.QPushButton(Form)
        self.pbOK.setGeometry(QtCore.QRect(190, 200, 113, 32))
        self.pbOK.setObjectName("pbOK")
        self.inputText = QtWidgets.QTextEdit(Form)
        self.inputText.setGeometry(QtCore.QRect(20, 20, 281, 51))
        self.inputText.setObjectName("inputText")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pbOK.setText(_translate("Form", "PushButton"))

