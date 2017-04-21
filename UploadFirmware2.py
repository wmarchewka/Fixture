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
        headers = {
            'authorization': "Basic ZmFjdG9yeTpmYWN0b3J5",
            'cache-control': "no-cache",
            'Accept - Language':'en-us',
            'Host: 10.0.0.210',
            'Content - Type: multipart/form-data',
            'boundary = ---------------------------7dd3201c5104d4',
            'Content - Length: 123632',
            'Connection: Keep - Alive',
            'Authorization':'Basic ZmFjdG9yeTpmYWN0b3J5',
        }''''''''''''''''''''''''''
        myfile = {"file": ("filexxx", open(path, "rb"))}

        response = requests.request("POST", verify=False, url=host, data=myfile, headers=headers)

        print(response.text)
    except Exception as e:
        print
        "Exception:", e


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