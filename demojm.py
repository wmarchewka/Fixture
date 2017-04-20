import mainwindow_auto


class ParseData(mainwindow_auto.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file
        self.txtSerialData.setText('test')

    def parse_incoming_data(t):

        self.txtSerialData.setText(t)
        print(t)

def main():
    pass


if __name__ == '__main__':
    main()
