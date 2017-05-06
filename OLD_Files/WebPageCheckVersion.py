import socket

def check_webpageversion(host):
    try:
        port = 23
        print('Checking webpage version...')
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(5)
        conn = host, port
        sc.connect(conn)
        sc.send(b'$login,factory,factory\r\n')
        data = sc.recv(100)
        print('login data-' + str(data))
        sc.send('')
        data = sc.recv(100)
        print('return data->' + str(data))



    except OSError as err:
        print(err)
        return False, err


def main():
    ip_add = '192.168.1.99'
    ret = check_webpageversion(ip_add)
    print(ret)

if __name__ == '__main__':
    main()