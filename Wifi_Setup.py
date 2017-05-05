import socket
import UploadFirmware
import BarCode as bc


def setup_wifi(host, new_mac):
    try:
        port = 23
        print('Starting WIFI Configuration ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(2)
        conn = host, port
        sc.connect(conn)
        data = sc.recv(100)
        print(data)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print(data)
        sc.send(b'$wlanmac,G\r\n')
        old_mac = sc.recv(100)
        old_mac = old_mac.decode().split(',')[2]
        old_mac = str(old_mac)
        if old_mac == 'N/A':
            print('No WIFI MAC Found')
        if new_mac:
            print('old_mac -> ' + str(old_mac))
            print('new_mac -> ' + new_mac)
            print('Setting new mac address...')
            se = '$wlanmac,S,' + new_mac + str('\r\n')
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
                ret = UploadFirmware.upload_file('wifi')

    except OSError as err:
        print(err)
        return False, err



def main():
    ip_add = '192.168.1.99'
    mac_add = ''
    ret = setup_wifi(ip_add, mac_add)
    print(ret)


if __name__ == '__main__':
    main()