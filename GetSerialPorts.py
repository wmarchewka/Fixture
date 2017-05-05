# import serial.tools.list_ports
# ports = list(serial.tools.list_ports.comports())
# for p in ports:
#    list.append(p)

import sys
import glob
import serial

def new_ports():
    settings = []
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        settings.append(p)
        print(p)
        return  settings


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    print("Searching for serial ports...")
    settings = []
    for port in ports:
        try:
            s = serial.Serial(port)
            #st = s.get_settings()
            s.close()
            settings.append(port)
            print('Found->' + port)
        except (OSError, serial.SerialException):
            pass
    return settings

def main():
    serial_ports()

if __name__ == '__main__':
    main()