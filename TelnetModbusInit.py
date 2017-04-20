# this will be used to connect and get voltage readings through telnet

import telnetlib


def ModbusInit(ip_add):
    print("Setting modbus defaults")
    PORT = 23
    TIMEOUT = 5
    tn = telnetlib.Telnet(host=ip_add, port=PORT, timeout=TIMEOUT)
    tn.write(b'$login,factory,factory\n')
    tn.write(b'$modbd,s,19200\n')
    tn.write(b'$modp,s,1\n')
    tn.write(b'$modst,s,1\n')
    tn.write(b'$reboot\n')
    tn.write(b'\r')
    tempdata = tn.read_all().decode('ascii')
    print(tempdata)
    tn.close()

    return tempdata


def __init__(self):
    super().__init__()
    self.initUI()


def main():
    #HOST = "10.0.0.210"
    HOST = '192.168.1.6'
    ret = ModbusInit(HOST)
    print(ret)


if __name__ == '__main__':
    main()
