import requests
import io
import GetOS as gs
import os

global osname
osname = gs.get_platform()

# with open( path + filename, 'rb') as f: r = requests.post('http://' + ip_address + /upload_file.cgi', data={'filename': filename, 'name': slot}, files={filename: f})

def file_size(fname):
    pass

def upload_file(host,fname,slot,path):
    try:
        f = open(path, "rb")
        fn = f.read(123632)
        url = 'http://' + host + '/upload_file.cgi'
        files  = ',data="filename": ' + path + ', "name":' +  slot
        print(url)
        r = requests.post(url, files=files)
        print(r)

    except OSError as err:
        print(err)
        return False, err


def main():

    global osname
    host = '192.168.1.8'
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