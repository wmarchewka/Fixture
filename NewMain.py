from ClassMain import MainWindow
from classPopupCombo import popupCombo


import sys
import threading
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    #form = MainWindow()
    #form.show()
    mc = MainWindow()
    pc = popupCombo()
    mc.make_connection(pc)
    mc.show()
    #pc.show()

    #gui_thread = threading.Thread(None,form.populate_defaults)
    #gui_thread.start()
    #form.lblStatus.setText('Ready...')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()