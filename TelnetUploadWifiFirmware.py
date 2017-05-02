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
    #print('filesize->' + str(statinfo.st_size))
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
        #print('fsize->' + str(fsize))
        filename = open(path, "br")
        fn = filename.read()

        myauthorization = base64.b64encode(b'factory:factory')

        my_req_body = "-----------------------------7dd3201c5104d4\r\n"
        my_req_body =  my_req_body + 'Content-Disposition: form-data; name="' + str(slot) + '"; filename="' + str(path) + '"\r\n'
        my_req_body =  my_req_body + 'Content-Type: application/octet-stream\r\n'
        my_req_body =  my_req_body + '\r\n\r\n'
        my_req_end = "\r\n-----------------------------7dd3201c5104d4\r\n"

        print('Length of body->' + str(len(my_req_body)))
        print('Length of file->' + str(fsize))
        print('Length of end->' + str(len(my_req_end)))

        totalsize = len(my_req_body) + fsize + len(my_req_end)
        print('Total size->' + str(totalsize))

        my_req_head = "POST /upload_file.cgi HTTP/1.1\r\n"
        my_req_head = my_req_head +  "Accept-Language: en-us\r\n"
        my_req_head = my_req_head + "Host: 192.168.1.100\r\n"
        my_req_head = my_req_head + "Content-Type: multipart/form-data; boundary=---------------------------7dd3201c5104d4\r\n"
        my_req_head = my_req_head + "Content-Length: " + str(totalsize) + "\r\n"
        my_req_head = my_req_head + "Connection: Keep-Alive\r\n"
        my_req_head = my_req_head + "Authorization: Basic ZmFjdG9yeTpmYWN0b3J5"# + str(myauthorization)
        my_req_head = my_req_head + "\r\n\r\n"
        my_req_head = my_req_head + "\r\n"

        sys.stdout.write(my_req_head)
        sys.stdout.write(my_req_body)
        sys.stdout.write(str(fn))
        sys.stdout.write(str(my_req_end))

        sc.send(my_req_head.encode('ascii'))
        sc.send(my_req_body.encode('ascii'))
        sc.send(fn)
        sc.send(my_req_end.encode('ascii'))


        data = sc.recv(500)
        print('return data-------------------------')
        print(data)


    except OSError as err:
        print(err)
        return False, err


def main():

    global osname
    #host = '192.168.1.99'
    host = '10.0.0.229'
    slot = 'web'
    print(osname)

    if osname == "Windows":
        path = r"C:web_pages_UEC025_ENG.tfs"
    elif osname == "OS X":
        path = os.path.expanduser("~/web_pages_UEC025_ENG.tfs")

    fname = 'web_pages_UEC025_ENG.tfs'
    ret = upload_file(host,fname,slot, path)
    print(ret)

if __name__ == '__main__':
    main()