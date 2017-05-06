import telnetlib
import socket
import time

def TelnetM40ButtonTest():
    try:
        host = "192.168.1.8"
        port = 23
        #HOST = '10.0.0.210'
        print('Starting button test on ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = host,port
        PORT = 23
        TIMEOUT = 5
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        #tn = telnetlib.Telnet(host=HOST, port=PORT, timeout=TIMEOUT)
        #tn.write(b'$login,factory,factory\n')
        #tn.write(b"$bts,s,0\n")
        #tn.write(b"$bts,G\n\r")
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$bts,s,0\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$bts,G\r\n')
        data = sc.recv(100)
        print(data)
        t = 0
        p = ''
        while True:
            sc.send(b'$bts,G\r\n')
            data = sc.recv(100)
            print(data)
            time.sleep(1)
            t = t + 1
            print ('t ' + str(t))
            if t == 25:
                break
            d = str(data).split(',')
            d = d[2]
            if p != d:
                t = 0
            p = d
            print( d.encode('ascii') )
            if d == '1':
                print('press button 1')
                r = 1
            if d == '2':
                print('press button 2')
            if d == '3':
                print('press button 3')
            if d == '4':
                print('press button 4')
            if d == '5':
                print('Unit passed button test')
                sc.close
                return True,"Unit passed Button Test"
        print("timeout")
        sc.close()
        False,"Timeout"


    except OSError as err:
        print(err)
        return False, err

def __init__(self):
    super().__init__()
    self.initUI()


def main():
    ret  = TelnetM40ButtonTest()
    print(ret)
    pass


if __name__ == '__main__':
    main()
