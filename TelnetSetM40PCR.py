# this will be used to connect and get voltage readings through telnet
# ensure voltages are in the range

import socket



def SetPCR(host):
    try:
        print("Setting PCR value on " + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 23
        conn = host, port
        sc.settimeout(2)
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$PCR,S,E0100110\r\n')
        data = sc.recv(100)
        print('data -> ' + str(data))
        data = data.decode().split(',')[3].find('OK')
        sc.close()
        if data > 0:
            print('PCR not set')
            return False, "PCR not set"
        else:
            print('PCR successfully set')
            return True, 'PCR successfully set'



    except socket.timeout as err:
        print('socket timeout')
        return False, err

    except socket.error as err:
        print('socket error')
        return False, err

    except OSError as err:
        sc.close
        print(err)
        return False, err



def main():
    ip_addr = '192.168.1.8'
    ret  = SetPCR(ip_addr)
    print(ret)



if __name__ == '__main__':
    main()
# this will be used to connect and get voltage readings through telnet
# ensure voltages are in the range
