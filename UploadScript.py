import socket

def write_script(host, path):
    try:
        port = 23
        print('Uploading script ' + path)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(5)
        conn = host, port
        script = open(path,'br')
        fn = script.read()
        print('file-> ' + str(fn))
        sc.connect(conn)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print('login data>' + str(data))
        splitdata = fn.split(b'\r\n')
        print(splitdata)
        for linedata in splitdata:
            sc.send(linedata + b'\r\n')
            data = sc.recv(1000)
            print('data->' + str(data))


    except OSError as err:
        print(err)
        return False, err


def main():
    ip_add = '192.168.1.99'
    path = r'C:\UEC\Functional Test\M50\Wi Fi No MB Default Script 062215.txt'
    ret = write_script(ip_add,path)
    print(ret)

if __name__ == '__main__':
    main()