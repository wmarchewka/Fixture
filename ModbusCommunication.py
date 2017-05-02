import minimalmodbus

def mbComm(comport,address):
    uut = minimalmodbus.Instrument(comport, address)
    uut.read_register(24, 1)
    uut.write_register(24, 450, 1)
    uut.read_register(24, 1)



def __init__(self):
    super().__init__()
    self.initUI()

def main():
    add = 1
    ret = bmComm(add)
    print(ret)

if __name__ == '__main__':
    main()
