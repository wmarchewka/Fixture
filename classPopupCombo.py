from QT_Project import popupSlot_auto as pw
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

# ****************************************************************************************************
class popupCombo(QMainWindow, pw.Ui_MainWindow):

    changedValue = pyqtSignal('QString')

    def __init__(self):
        super(popupCombo, self).__init__()
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
        self.comboBox.currentIndexChanged.connect(self.comboonactivated)
        self.pbgobutton.clicked.connect(self.gobutton)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.setCurrentIndex(0)

    def comboonactivated(self):
        self.indexstr = self.comboBox.currentText()
        self.index = self.comboBox.currentIndex()


    def gobutton(self):
        print("Uploading filetype " + str(self.indexstr))
        self.comboBox.setCurrentIndex(self.index)
        self.changedValue.emit(self.indexstr)
        #self.close()
        #mw=MainWindow()
        #mw.upload_interrim(self.indexstr)
        #gui_thread = threading.Thread(None, MainWindow().uploadfile_command(self.indexstr))
        #gui_thread.start()

    # ****************************************************************************************************