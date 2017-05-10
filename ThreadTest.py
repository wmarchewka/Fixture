import sys
import threading
from PyQt5 import QtWidgets
from QT_Project import mainwindow_auto as mw
from PyQt5.QtWidgets import QApplication
import EthernetCommLibrary as el

def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug

class MainWindow(QtWidgets.QMainWindow, mw.Ui_MainWindow):   #QMainWindow, mw.Ui_MainWindow
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # gets defined in the UI file

        self.pbSendTelnet.clicked.connect(self.pressedResetButton)
        self.pbDoPing.clicked.connect(self.PingUUT)
        self.lblStatus.setText('Welcome')

    def PingUUT(self):
        pass

    def pressedResetButton(self):
        print("Pressed reset button")
        self.lblStatus.setText("Button test running...")
        gui_thread = threading.Thread(None, self.ButtonTest ,None)
        gui_thread.start()

    def ButtonTest(self):
        self.lblStatus.setText("Button test running...")
        el.EthComLib.m40_buttontest(self)

def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
