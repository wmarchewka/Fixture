import requests
from requests import Request, Session
import io
import GetOS as gs
import os

global osname
osname = gs.get_platform()

# with open( path + filename, 'rb') as f: r = requests.post('http://' + ip_address + /upload_file.cgi', data={'filename': filename, 'name': slot}, files={filename: f})

def file_size(fname):
    pass

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def upload_file(host, fname, slot, path):
    headers = {'Accept-Language':'en-us', 'Host':'10.0.0.210',  'Content-Disposition':'form-data; name="' + slot + '"; filename="' + path + '"'}
    #mydata = {'name': slot, 'filename': path}

    myfile = {'web': (fname, open(fname, 'rb'), 'application/octet-stream')}
    #response = requests.request("POST", url=host, files=myfile, headers=headers, auth=('factory', 'factory'))
    response = Request("POST", url=host, files=myfile, headers=headers, auth=('factory', 'factory'))
    #response = Request("POST", url=host, files=myfile, data=mydata, auth=('factory', 'factory'))
    pretty_print_POST(response.prepare())

    #print("response")
    #print(response.status_code)

    #print("response text")
    #print(response.text)

    #print("response header")
    #print(response.headers)


# except Exception as e:
#    print("Exception:", e)


def main():

    global osname
    #host = 'http://192.168.1.5'
    host = 'http://10.0.0.148/upload_file.cgi'
    slot = 'web'
    print(osname)

    if osname == "Windows":
        path = r"C:\UEC\Functional Test\M50\Configuration\web_pages_UEC_AC_025_SPN.tfs"
    elif osname == "OS X":
        path = os.path.expanduser("~/web_pages_UEC_AC_025_SPN.tfs")

    fname = 'web_pages_UEC_AC_025_SPN.tfs'
    ret = upload_file(host,fname,slot, path)
    print(ret)

if __name__ == '__main__':
    main()