# this will be used to connect and get voltage readings through telnet
# ensure voltages are in the range

import telnetlib


def GetTelnetVoltages():
    try:
        HOST = "192.168.1.6"
        #HOST = '192.168.1.99'
        print("Getting Voltages from " + HOST)
        PORT = 23
        TIMEOUT = 5
        tn = telnetlib.Telnet(host=HOST, port=PORT, timeout=TIMEOUT)
        tn.set_debuglevel(0)
        tn.write(b"$login,factory,factory\n")
        tn.write(b"$mdra,0,U0512,U377520\n")
        tn.write(b"$mdra,0,U0513,U377520\n")
        tn.write(b"$mdra,0,U0514,U377520\n")
        tn.write(b"$mdra,0,215,000000C0\n")
        tn.write(b"$mdra,0,U0007\n")
        tn.write(b"$mdra,0,U0008\n")
        tn.write(b"$mdra,0,U0009\n")
         # TODO need to scale these values upon return
        tn.write(b"$mdra,0,U0518,U5000\n")
        tn.write(b"$mdra,0,U0519,U5000\n")
        tn.write(b"$mdra,0,U0520,U5000\n")
        tn.write(b"$mdra,0,U0521,U5000\n")
        tn.write(b"$mdra,0,U0522,U5000\n")
        tn.write(b"$mdra,0,U0523,U5000\n")
        tn.write(b"$mdra,0,215,000000C0\n")
        # TODO need burden resistor value from config
        tn.write(b"$mdra,0,U0018\n")
        tn.write(b"$mdra,0,U0026\n")
        tn.write(b"$mdra,0,U0034\n")
        tn.write(b"$mdra,0,U0042\n")
        tn.write(b"$mdra,0,U0050\n")
        tn.write(b"$mdra,0,U0058\n")
        tn.write(b"\r")
        tempdata = tn.read_all().decode('ascii')
        tn.close()
        tempdata = tempdata.split(',')
        voltageA = float(tempdata[tempdata.index('U0007') + 1]) / 1000
        voltageB = float(tempdata[tempdata.index('U0008') + 1]) / 1000
        voltageC = float(tempdata[tempdata.index('U0009') + 1]) / 1000
        currentA = float(tempdata[tempdata.index('U0018') + 1]) / 1000
        currentAneg = float(tempdata[tempdata.index('U0026') + 1]) / 1000
        currentB = float(tempdata[tempdata.index('U0034') + 1]) / 1000
        currentBneg = float(tempdata[tempdata.index('U0042') + 1]) / 1000
        currentC = float(tempdata[tempdata.index('U0050') + 1]) / 1000
        currentCneg = float(tempdata[tempdata.index('U0058') + 1]) / 1000
        print(voltageA,voltageB,voltageC)
        print(currentA,currentAneg,currentB,currentBneg,currentC,currentCneg)
        return True,tempdata


    except OSError as err:
        #tn.close
        print(err)
        return False, err

def __init__(self):
    super().__init__()
    self.initUI()


def main():
    ret  = GetTelnetVoltages()
    print(ret)
    pass


if __name__ == '__main__':
    main()
