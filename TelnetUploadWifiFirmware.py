import socket
import os
import base64
import GetOS as gs
import sys

global osname
osname = gs.get_platform()


def file_size(fname):
    import os
    statinfo = os.stat(fname)
    print('filesize->' + str(statinfo.st_size))
    return statinfo.st_size

def upload_file(host,fname,slot,path):
    try:
        port = 80
        print('Starting uploading of file to  ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(5)
        conn = host, port
        sc.connect(conn)

        fsize = file_size(path)
        fsize = 123632
        filename = open(path, "br")
        fn = filename.read(fsize)

        myauthorization = base64.b64encode(b'factory:factory')

        my_req_body = "-----------------------------7dd3201c5104d4\r\n"
        my_req_body = my_req_body  + 'Content-Disposition: form-data; name="' + str(slot) + '"; filename="' + str(fname) + '"\r\n'
        my_req_body = my_req_body  + 'Content-Type: application/octet-stream\r\n'
        my_req_body = my_req_body  + '\r\n'

        my_req_body = my_req_body + str(fn)

        my_req_body = my_req_body +  "-----------------------------7dd3201c5104d4\r\n"
        fsize = file_size(path)
        fsize = '123632'
        my_req_head = "POST /upload_file.cgi HTTP/1.1\r\n"
        my_req_head = my_req_head +  "Accept-Language: en-us\r\n"
        #print(my_req_head)
        my_req_head = my_req_head + "Host: 192.168.1.100\r\n"
        my_req_head = my_req_head + "Content-Type: multipart/form-data; boundary=---------------------------7dd3201c5104d4\r\n"
        my_req_head = my_req_head + "Content-Length: " + str(fsize) + "\r\n"
        my_req_head = my_req_head + "Connection: Keep-Alive\r\n"
        my_req_head = my_req_head + "Authorization: Basic ZmFjdG9yeTpmYWN0b3J5"# + str(myauthorization)
        my_req_head = my_req_head + "\r\n\r\n"
        my_req_head = my_req_head + "\r\n"

        sys.stdout.write(my_req_head)
        sys.stdout.write(my_req_body)

        total =  my_req_head + my_req_body
        sc.send(total.encode('ascii'))

        data = sc.recv(500)
        print('return data-------------------------')
        print(data)


    except OSError as err:
        print(err)
        return False, err


def main():

    global osname
    host = '192.168.1.5'
    #host = '10.0.0.210'
    slot = 'web'
    print(osname)

    if osname == "Windows":
        path = r"C:\UEC\Functional Test\M50\Configuration\web_pages_UEC025_ENG.tfs"
    elif osname == "OS X":
        path = os.path.expanduser("~/web_pages_UEC025_ENG.tfs")

    fname = 'web_pages_UEC025_ENG.tfs'
    ret = upload_file(host,fname,slot, path)
    print(ret)

if __name__ == '__main__':
    main()