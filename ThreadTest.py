import sys
import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from QT_Project import mainwindow_auto as mw
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget
import EthernetCommLibrary as el
import time

def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug

class WorkerThread(QtCore.QThread):

    #job_done = QtCore.pyqtSignal('QString')

    def __init__(self, method_to_run):
        super(WorkerThread, self).__init__()
        self.method = method_to_run
        self.gui_text = None

    def run(self):
        self.method()

class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):   #QMainWindow, mw.Ui_MainWindow
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # gets defined in the UI file
        self.pbSendTelnet.clicked.connect(self.pressedResetButton)
        self.pbDoPing.clicked.connect(self.PingUUT)

    def pressedResetButton(self):
        print("Pressed reset button")
        #self.worker_thread.job_done.connect(self.on_job_done)
        self.worker_thread = WorkerThread(self.ButtonTest)
        self.worker_thread.gui_text = self.lblStatus.text
        self.worker_thread.start()
        #el.EthComLib.check_reset_button(self.worker_thread, '192.168.1.99')

    def PingUUT(self):
        print("Pressed reset button")
        self.worker_thread = WorkerThread(self.ButtonTest)
        self.worker_thread.job_done.connect(self.on_job_done)
        self.worker_thread.gui_text = self.lblStatus.text
        self.worker_thread.start(self)

    @staticmethod
    def ButtonTest():
        while True:
            el.EthComLib.check_reset_button('test','192.168.1.99')
            
    def on_job_done(self, generated_str):
        print("Generated string : ", generated_str)
        self.lblStatus.setText(generated_str)



def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
