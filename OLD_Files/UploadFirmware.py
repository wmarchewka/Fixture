import base64
import os
import socket

from OLD_Files import Configuration as cf, GetOS as gs

global osname
osname = gs.get_platform()

def file_size(fname):
    import os
    statinfo = os.stat(fname)
    return statinfo.st_size

def upload_file(slot):
    try:
        boardtype = cf.config_read('UUT',"major_board_type")
        if boardtype == "M40":
            section = 'M40_FOLDERS'
        if boardtype == "M50":
            section = 'M50_FOLDERS'
        if boardtype == "M60":
            section = 'M60_FOLDERS'

        if slot == 'wifi':
            key = 'm40_wifi_firmware'
        if slot == 'web':
            key = 'm40_web_page_upload'
        if slot == 'meter':
            key = 'm40_meter_ic_firmware'
        if slot == 'firmware':
            key = 'm40_firmware'

        path = cf.config_read(section, key)
        host = cf.config_read('TELNET',"ip_address")
        user = 'factory'
        password = 'factory'
        port = 80
        logger.debug('Starting uploading of file ' + path + ' to  ' + host)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.settimeout(5)
        conn = host, port
        sc.connect(conn)

        fsize = file_size(path)
        filename = open(path, "br")
        fn = filename.read()

        myauthorization = base64.b64encode(user.encode('ascii') + b":" + password.encode('ascii'))

        my_req_body = "-----------------------------7dd3201c5104d4\r\n"
        my_req_body =  my_req_body + 'Content-Disposition: form-data; name="' + str(slot) + '"; filename="' + str(path) + '"\r\n'
        my_req_body =  my_req_body + 'Content-Type: application/octet-stream'
        my_req_body =  my_req_body + '\r\n\r\n'
        my_req_end = "\r\n-----------------------------7dd3201c5104d4\r\n"

        logger.debug('Length of body->' + str(len(my_req_body)))
        logger.debug('Length of file->' + str(fsize))
        logger.debug('Length of end->' + str(len(my_req_end)))

        totalsize = len(my_req_body) + fsize + len(my_req_end)
        logger.debug('Total size->' + str(totalsize))

        my_req_head = "POST /upload_file.cgi HTTP/1.1\r\n"
        my_req_head = my_req_head + "Accept-Language: en-us\r\n"
        my_req_head = my_req_head + "Host: " + str(host) + "\r\n"
        my_req_head = my_req_head + "Content-Type: multipart/form-data; boundary=---------------------------7dd3201c5104d4\r\n"
        my_req_head = my_req_head + "Content-Length: " + str(totalsize) + "\r\n"
        my_req_head = my_req_head + "Connection: Keep-Alive\r\n"
        my_req_head = my_req_head + "Authorization: Basic " + str(myauthorization,'utf-8')      #    ZmFjdG9yeTpmYWN0b3J5"
        my_req_head = my_req_head + "\r\n\r\n"
        my_req_head = my_req_head + "\r\n"

        #sys.stdout.write(my_req_head)
        #sys.stdout.write(my_req_body)
        #sys.stdout.buffer.write(fn)
        #sys.stdout.write(str(my_req_end))

        buffer = my_req_head.encode('ascii') + my_req_body.encode('ascii')
        while buffer:
            bytes = sc.send(buffer)
            buffer = buffer[bytes:]
        data = sc.recv(250)
        logger.debug('return data-------------------------')
        logger.debug(data)

        buffer = fn
        while buffer:
            bytes = sc.send(buffer)
            buffer = buffer[bytes:]
        data = sc.recv(1000)
        logger.debug('return data-------------------------')
        logger.debug(data)

        buffer = my_req_end.encode('ascii')
        while buffer:
            bytes = sc.send(buffer)
            buffer = buffer[bytes:]
        data = sc.recv(500)
        logger.debug('return data-------------------------')
        #data = str(data)
        logger.debug(data)
        data = sc.recv(500)
        logger.debug('return data-------------------------')
        logger.debug(data)
        data = str(data)
        sc.close()
        if data.find('url=upload.html'):
            logger.debug('upload sucessful')
        else:
            logger.debug('upload failed')

    except OSError as err:
        logger.debug(err)
        return False, err


def main():
    global osname
    slot = 'web'
    logger.debug(osname)
    if osname == "Windows":
        path = r"C:\web_pages_UEC_AC_025_ENG.tfs"
    elif osname == "OS X":
        path = os.path.expanduser("~/web_pages_UEC025_ENG.tfs")
    ret = upload_file(slot)
    logger.debug(ret)

if __name__ == '__main__':
    main()