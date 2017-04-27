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

        headers = {'Content-Disposition ' :'form-data; name="' + slot +'"; filename="' + path + '"' }

        myfile = {"file": open(path, "rb")}

        response = requests.request("POST", url=host, files=myfile, headers=headers, auth=('factory','factory') )

        print("response")
        print (response.status_code)

        print("response text")
        print(response.text)

        print("response header")
        print(response.headers)

    #except Exception as e:
    #    print("Exception:", e)


def main():

    global osname
    host = 'http://192.168.1.5'
    #host = '10.0.0.210'
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