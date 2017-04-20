import socket
import os
import base64



def open_file_bin_mode(fname):
    f = open(fname,"rb")
    myreq_body = f

def file_size(fname):
    import os
    statinfo = os.stat(fname)
    print('filesize->' + str(statinfo.st_size))
    return statinfo.st_size

def upload_file(host,fname,slot):
    try:
        filename = open_file_bin_mode(fname)
        fsize = file_size(fname)
        port = 80
        print('Starting uploading of file to  ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(5)
        conn = host, port
        # sc.connect(conn)

        myauthorization = base64.b64decode(b'factory:factory', 'utf-8')
        # encoded = base64.b64encode(b'data to be encoded')

        my_req_body = "-----------------------------7dd3201c5104d4\r\n"

        my_req_head = "POST /upload_file.cgi HTTP/1.1\r\n"
        my_req_head = my_req_head + "Accept-Language: en-us\r\n"
        my_req_head = my_req_head + "Host: 192.168.1.100\r\n"
        my_req_head = my_req_head + "Content-Type: multipart/form-data; boundary=---------------------------7dd3201c5104d4\r\n"
        my_req_head = my_req_head + "Content-Length: " + str(fsize) + "\r\n"
        my_req_head = my_req_head + "Connection: Keep-Alive\r\n"
        my_req_head = my_req_head + "Authorization: Basic " + myauthorization
        my_req_head = my_req_head + "\r\n\r\n"
        my_req_head = my_req_head + "\r\n"

        my_req_body = my_req_body  + "Content-Disposition: form-data; name=\\" + slot + "\\; filename=\\" + filename + "\r\n"
        my_req_body = my_req_body  + "Content-Type: application/octet-stream\r\n"
        my_req_body = my_req_body  + "\r\n"

        print (my_req_head + my_req_body)
        #sc.send(my_req_head + my_req_body)


    except OSError as err:
        print(err)
        return False, err


def main():
    host = '192.168.1.8'
    slot = 'wifi'
    fname = r"C:\UEC\Functional Test\M50\Configuration\web_pages_UEC023_ENG.tfs"
    ret = upload_file(host,fname,slot)
    print(ret)

if __name__ == '__main__':
    main()