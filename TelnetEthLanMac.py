import socket

def write_lan_mac(ip_add):
    try:
        host = "192.168.1.8"
        port = 23
        print('Starting button test on ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(2)
        conn = host, port
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$lanmac,G\r\n')
        old_mac = sc.recv(100)
        old_mac = old_mac.decode().split(',')[2]
        print('old_mac -> ' + old_mac)
        old_mac = str(old_mac)
        new_mac = old_mac
        print('new_mac -> ' + new_mac)
        se = '$lanmac,S,' + new_mac + str('\r\n')
        sc.send(se.encode())
        data = sc.recv(100)
        print('data->' + str(data))
        result = data.decode().split(',')[3].find('OK')
        print('result->' + str(result))
        if result > 0:
            print('Lan Mac not set')
            return False, "Lan Mac not set"
        else:
            print('Lan Mac successfully set')
            return True, 'Lan Mac successfully set'

    except OSError as err:
        print(err)
        return False, err


def main():
    ip_add = '192.168.1.6'
    ret = write_lan_mac(ip_add)
    print(ret)

if __name__ == '__main__':
    main()