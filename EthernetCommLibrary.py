import base64
import os
import socket
import telnetlib
import time

import FileConfigurationLibrary as fl
import SupportLibrary as sl
global osname
osname = sl.getOsPlatform()

#TODO make sure to come up with a way to get ip address from config file

class EthComLib(object):

    def __init__(self):
        print('EthComLib class is initializing')

    #******************************************************************************************
    def pinguut(self=None, ip_add=None, numpings=1):
        pingcount = 0

        while True:
            print("pinging UUT at ip " + ip_add +' count ' +  str(pingcount))
            self.lblStatus.setText("pinging UUT at ip " + ip_add +' count ' +  str(pingcount))
            if sl.getOsPlatform() =='Linux':
                data = ('ping '+ ip_add + ' -w 1000 -c 1')  # set ping timeout to 1000ms
            elif sl.getOsPlatform() =='Windows':
                data = ('ping '+ ip_add + ' -w 1000 -n 1')
            elif sl.getOsPlatform() == 'OSX':
                data = ('ping ' + ip_add + ' -W 1000 -c 1')
            response = os.system(data)              #default ping takes 3 secs to respond
            print(response)
            if response == 0:
                print(ip_add + ' is up!')
                self.lblStatus.setText(ip_add + ' is up!')
                return True, ip_add + ' is up!'
            else:
                print(ip_add + ' is down!')
                self.lblStatus.setText(ip_add + ' is down!')
                pingcount = pingcount + 1
                if pingcount > numpings:
                    return False, ip_add + ' is down!'

    #******************************************************************************************
    def check_reset_button(self, ip_add):
        update = ''
        timecounter = 0
        respond_initial = False
        reset = False
        while  True:
            val = EthComLib.pinguut(self, ip_add, 1)
            print('val->' + str(val))
            if val[0] == True and reset == True:
                print("Successfully reset...")
                update = ('Successfully reset...')
                self.lblStatus.setText(update)
                return True, "Successfully reset..."
            if val[0] == True:
                timecounter = timecounter + 1
                respond_initial = True
                print('Press reset button. Waiting ' + str(timecounter) + ' seconds')
                update = ('Press reset button.  Waiting ' + str(timecounter) + ' seconds')
                self.lblStatus.setText(update)
                time.sleep(1.0)
                if timecounter == 5:
                    print('Timedout waiting for button press...')
                    update = ('Timed out waiting for button press...')
                    self.lblStatus.setText(update)
                    return False, 'Timed out waiting for button press'
            if not respond_initial:
                print('Did not respond to initial ping...')
                update = ('Did not respond to initial ping...')
                return False,  'Did not respond to initial ping'
            if respond_initial == True and val[0] == False:
                print ('Unit resetting...')
                update = ('Unit resetting...')
                reset = True
            print('respond initial->' + str(respond_initial))
            print('')
            self.lblStatus.setText(update)

    #******************************************************************************************
    def write_lan_mac(self, ip_add):
        try:
            host = ip_add
            port = 23
            print('Setting LAN MAC address on ' + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = host, port
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            sc.write(b'$lanmac,G\r\n')
            old_mac = sc.recv(100)
            old_mac = old_mac.decode().split(',')[2]
            print('old_mac -> ' + old_mac)
            old_mac = str(old_mac)
            new_mac = old_mac
            print('new_mac -> ' + new_mac)
            self.lblStatus.setText('Old MAC : ' + str(old_mac) + '     New MAC : ' + str(new_mac))
            se = '$lanmac,S,' + new_mac + str('\r\n')
            sc.write(se.encode())
            data = sc.recv(100)
            print('data->' + str(data))
            result = data.decode().split(',')[3].find('OK')
            print('result->' + str(result))
            if result > 0:
                print('Lan Mac not set')
                return False, "Lan Mac not set"
                self.lblStatus.setText('Lan MAC not set')
            else:
                print('Lan Mac successfully set')
                return True, 'Lan Mac successfully set'
                self.lblStatus.setText('Lan MAC successfully set')

        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def getvoltages(self, ip_add):
        try:
            print("Getting Voltages from " + ip_add)
            self.lblStatus.setText("Getting voltages from " + ip_add)
            tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = ip_add, 23
            tn.connect(conn)
            tn.send(b"\n")
            tempdata = tn.recv(100)
            tn.send(b"$login,factory,factory\n")
            tempdata = tn.recv(50)
            print(str(tempdata))
            tn.send(b"$mdra,0,U0018\n")         # use this to see if a slip error returns
            tempdata = tn.recv(100)
            print(str(tempdata))
            slip_err = tempdata.find(b'SLIP_DRIVER_ERROR_READ_TIMEOUT')
            tempdata = ''
            if slip_err >=0:
                print('SLIP driver error')
                self.lblStatus.setText('Failed to get voltages.  SLIP Error')
                return False, 'Failed to get voltages.  SLIP Error'
            else:
                tn.close()
                PORT = 23
                TIMEOUT = 5
                tn = telnetlib.Telnet(host=ip_add, port=PORT, timeout=TIMEOUT)
                tn.write(b'$login,factory,factory\n')
                tn.write(b"$mdra,0,U0512,U377520\n")
                tn.write(b"$mdra,0,U0513,U377520\n")
                tn.write(b"$mdra,0,U0514,U377520\n")
                tn.write(b"$mdra,0,215,000000C0\n")
                tn.write(b"$mdra,0,U0007\n")
                tn.write(b"$mdra,0,U0008\n")
                tn.write(b"$mdra,0,U0009\n")
                 # TODO need to scale these values upon return
                tn.write(b"$mdra,0,U0518,U5000\n")
                tn.write(b"$mdra,0,U0519,U5000\n")
                tn.write(b"$mdra,0,U0520,U5000\n")
                tn.write(b"$mdra,0,U0521,U5000\n")
                tn.write(b"$mdra,0,U0522,U5000\n")
                tn.write(b"$mdra,0,U0523,U5000\n")
                tn.write(b"$mdra,0,215,000000C0\n")
                # TODO need burden resistor value from config
                tn.write(b"$mdra,0,U0018\n")
                tn.write(b"$mdra,0,U0026\n")
                tn.write(b"$mdra,0,U0034\n")
                tn.write(b"$mdra,0,U0042\n")
                tn.write(b"$mdra,0,U0050\n")
                tn.write(b"$mdra,0,U0058\n")
                tn.write(b"\r")
                tempdata = tn.read_all()
                print(tempdata)
                #tn.close()
                tempdata = str(tempdata)
                tempdata = tempdata.split(',')
                voltageA = float(tempdata[tempdata.index('U0007') + 1]) / 1000
                voltageB = float(tempdata[tempdata.index('U0008') + 1]) / 1000
                voltageC = float(tempdata[tempdata.index('U0009') + 1]) / 1000
                currentA = float(tempdata[tempdata.index('U0018') + 1]) / 1000
                currentAneg = float(tempdata[tempdata.index('U0026') + 1]) / 1000
                currentB = float(tempdata[tempdata.index('U0034') + 1]) / 1000
                currentBneg = float(tempdata[tempdata.index('U0042') + 1]) / 1000
                currentC = float(tempdata[tempdata.index('U0050') + 1]) / 1000
                currentCneg = float(tempdata[tempdata.index('U0058') + 1]) / 1000
                print(voltageA,voltageB,voltageC)
                print(currentA,currentAneg,currentB,currentBneg,currentC,currentCneg)
                data =  ("Voltages acquired from " + ip_add + '\n\r' + 'L1: ' + str(voltageA) + '  L2: ' + str(voltageB) + '  L3: ' +str(voltageC))
                self.lblStatus.setText(data)
                #TODO need to log this data in log
                return True,tempdata

        except OSError as err:
             tn.close
             print(err)
             return False, err
        except:
             tn.close
             return False, 'General Error'


#******************************************************************************************
    def m40buttontest(self):
        try:
            host = "192.168.1.99"
            port = 23
            #HOST = '10.0.0.210'
            print('Starting button test on ' + host)
            self.lblStatus.setText('Starting button test on ' + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = host,port
            PORT = 23
            TIMEOUT = 5
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            #tn = telnetlib.Telnet(host=HOST, port=PORT, timeout=TIMEOUT)
            #tn.write(b'$login,factory,factory\n')
            #tn.write(b"$bts,s,0\n")
            #tn.write(b"$bts,G\n\r")
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            sc.write(b'$bts,s,0\r\n')
            data = sc.recv(100)
            print(data)
            sc.write(b'$bts,G\r\n')
            data = sc.recv(100)
            print(data)
            t = 0
            p = ''
            while True:
                sc.write(b'$bts,G\r\n')
                data = sc.recv(100)
                print(data)
                time.sleep(1)
                t = t + 1
                print ('t ' + str(t))
                if t == 25:
                    break
                d = str(data).split(',')
                d = d[2]
                if p != d:
                    t = 0
                p = d
                print( d.encode('ascii') )
                if d == '1':
                    print('Press Button 1')
                    self.lblStatus.setText('Press Button 1')
                    r = 1
                if d == '2':
                    print('press button 2')
                    self.lblStatus.setText('Press Button 2')
                if d == '3':
                    print('press button 3')
                    self.lblStatus.setText('Press Button 3')
                if d == '4':
                    print('press button 4')
                    self.lblStatus.setText('Press Button 4')
                if d == '5':
                    print('Unit passed button test')
                    self.lblStatus.setText('Unit passed button test')
                    sc.close
                    return True,"Unit passed Button Test"
            print("timeout")
            sc.close()
            False,"Timeout"


        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def modbusinit(ip_add):
        print("Setting modbus defaults")
        PORT = 23
        TIMEOUT = 5
        tn = telnetlib.Telnet(host=ip_add, port=PORT, timeout=TIMEOUT)
        tn.write(b'$login,factory,factory\n')
        tn.write(b'$modbd,s,19200\n')
        tn.write(b'$modp,s,1\n')
        tn.write(b'$modst,s,1\n')
        tn.write(b'$reboot\n')
        tn.write(b'\r')
        tempdata = tn.read_all().decode('ascii')
        print(tempdata)
        tn.close()

        return tempdata
    #******************************************************************************************
    def setpcr(host):
        try:
            print("Setting PCR value on " + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = 23
            conn = host, port
            sc.settimeout(2)
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            sc.write(b'$PCR,S,E0100110\r\n')
            data = sc.recv(100)
            print('data -> ' + str(data))
            data = data.decode().split(',')[3].find('OK')
            sc.close()
            if data > 0:
                print('PCR not set')
                return False, "PCR not set"
            else:
                print('PCR successfully set')
                return True, 'PCR successfully set'

        except socket.timeout as err:
            print('socket timeout')
            return False, err

        except socket.error as err:
            print('socket error')
            return False, err

        except OSError as err:
            sc.close
            print(err)
            return False, err

    #******************************************************************************************
    def write_serialnumber(host):
        try:
            #TODO this needs finished
            port = 23
            print('Starting button test on ' + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = host, port
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            sc.write(b'$wlanmac,G\r\n')
            old_mac = sc.recv(100)
            old_mac = old_mac.decode().split(',')[2]
            print('old_mac -> ' + old_mac)
            old_mac = str(old_mac)
            new_mac = old_mac
            print('new_mac -> ' + new_mac)
            se = '$wlanmac,S,' + new_mac + str('\r\n')
            sc.write(se.encode())
            data = sc.recv(100)
            print('data->' + str(data))
            result = data.decode().split(',')[3].find('OK')
            print('result->' + str(result))
            if result > 0:
                print('Wireless lan mac not set')
                return False, "Wireless lan mac not set"
            else:
                print('Wireless lan mac successfully set')
                return True, 'Wireless lan mac successfully set'

        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def write_wifi_mac(host):
        try:
            port = 23
            print('Setting wireless LAN MAC ' + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = host, port
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            sc.write(b'$wlanmac,G\r\n')
            old_mac = sc.recv(100)
            old_mac = old_mac.decode().split(',')[2]
            print('old_mac -> ' + old_mac)
            old_mac = str(old_mac)
            new_mac = old_mac
            print('new_mac -> ' + new_mac)
            se = '$wlanmac,S,' + new_mac + str('\r\n')
            sc.write(se.encode())
            data = sc.recv(100)
            print('data->' + str(data))
            result = data.decode().split(',')[3].find('OK')
            print('result->' + str(result))
            if result > 0:
                print('Wireless lan mac not set')
                return False, "Wireless lan mac not set"
            else:
                print('Wireless lan mac successfully set')
                return True, 'Wireless lan mac successfully set'

        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def file_size(fname):
        import os
        statinfo = os.stat(fname)
        return statinfo.st_size

    #******************************************************************************************
    def upload_file(slot):
        try:
            boardtype = fl.configfileRead('UUT',"major_board_type")
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

            path = fl.configfileRead(section, key)
            host = fl.configfileRead('TELNET',"ip_address")
            user = 'factory'
            password = 'factory'
            port = 80
            print('Starting uploading of file ' + path + ' to  ' + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(5)
            conn = host, port
            sc.connect(conn)

            fsize =  EthComLib.file_size(path)
            filename = open(path, "br")
            fn = filename.read()

            myauthorization = base64.b64encode(user.encode('ascii') + b":" + password.encode('ascii'))

            my_req_body = "-----------------------------7dd3201c5104d4\r\n"
            my_req_body =  my_req_body + 'Content-Disposition: form-data; name="' + str(slot) + '"; filename="' + str(path) + '"\r\n'
            my_req_body =  my_req_body + 'Content-Type: application/octet-stream'
            my_req_body =  my_req_body + '\r\n\r\n'
            my_req_end = "\r\n-----------------------------7dd3201c5104d4\r\n"

            print('Length of body->' + str(len(my_req_body)))
            print('Length of file->' + str(fsize))
            print('Length of end->' + str(len(my_req_end)))

            totalsize = len(my_req_body) + fsize + len(my_req_end)
            print('Total size->' + str(totalsize))

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
                bytes = sc.write(buffer)
                buffer = buffer[bytes:]
            data = sc.recv(250)
            print('return data-------------------------')
            print(data)

            buffer = fn
            while buffer:
                bytes = sc.write(buffer)
                buffer = buffer[bytes:]
            data = sc.recv(1000)
            print('return data-------------------------')
            print(data)

            buffer = my_req_end.encode('ascii')
            while buffer:
                bytes = sc.write(buffer)
                buffer = buffer[bytes:]
            data = sc.recv(500)
            print('return data-------------------------')
            #data = str(data)
            print(data)
            data = sc.recv(500)
            print('return data-------------------------')
            print(data)
            data = str(data)
            sc.close()
            if data.find('url=upload.html'):
                print('upload sucessful')
            else:
                print('upload failed')

        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def write_script(host, path):
        try:
            port = 23
            print('Uploading script ' + path)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(5)
            conn = host, port
            script = open(path,'br')
            fn = script.read()
            print('file-> ' + str(fn))
            sc.connect(conn)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print('login data>' + str(data))
            splitdata = fn.split(b'\r\n')
            print(splitdata)
            for linedata in splitdata:
                sc.write(linedata + b'\r\n')
                data = sc.recv(1000)
                print('data->' + str(data))


        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def check_webpageversion(host):
        try:
            #TODO this needs finished
            port = 23
            print('Checking webpage version...')
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(5)
            conn = host, port
            sc.connect(conn)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print('login data-' + str(data))
            sc.write('')
            data = sc.recv(100)
            print('return data->' + str(data))



        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def setup_wifi(host, new_mac):
        try:
            #TODO enusre this is able to set wifi ssid and other things needed
            port = 23
            print('Starting WIFI Configuration ' + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = host, port
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            sc.write(b'$wlanmac,G\r\n')
            old_mac = sc.recv(100)
            old_mac = old_mac.decode().split(',')[2]
            old_mac = str(old_mac)
            if old_mac == 'N/A':
                print('No WIFI MAC Found')
                return False, "No WIFI MAC found"
            else:
                print("Current MAC " + old_mac)
            if new_mac:
                print('old_mac -> ' + str(old_mac))
                print('new_mac -> ' + new_mac)
                print('Setting new mac address...')
                se = '$wlanmac,S,' + new_mac + str('\r\n')
                sc.write(se.encode())
                data = sc.recv(100)
                print('data->' + str(data))
                result = data.decode().split(',')[3].find('OK')
                print('result->' + str(result))
                if result > 0:
                    print('Lan Mac not set')
                    return False, "Lan Mac not set"
                else:
                    print('Lan Mac successfully set')
                    ret = upload_file('wifi')

                    print(ret)

        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
def main():

    ip_add = '192.168.1.99'
    mac_add = '58:2f:42:20:00:01'
    path = r'C:\UEC\Functional Test\M50\Wi Fi No MB Default Script 062215.txt'
    module = 'A'

    if module == "A":
        ret = setup_wifi(ip_add, mac_add)

    if module == "B":
        ret = check_webpageversion(ip_add)

    if module == "C":
        ret = write_script(ip_add,path)

    if module == "D":
        global osname
        slot = 'web'
        print(osname)
        if osname == "Windows":
            path = r"C:\web_pages_UEC_AC_025_ENG.tfs"
        elif osname == "OS X":
            path = os.path.expanduser("~/web_pages_UEC025_ENG.tfs")
        ret = upload_file(slot)

    if module == "E":
        ret = write_wifi_mac(ip_add)

    if module == "F":
        ret = write_serialnumber(ip_add)

    if module == "G":
        ret = setpcr(ip_add)

    if module == "H":
        ret = modbusinit(ip_add)

    if module == "I":
        ret  = m40buttontest()

    if module == "J":
        ret = getvoltages()

    if module == "K":
        ret = write_lan_mac(ip_add)

    if module == "L":
        global respond_initial
        global reset
        respond_initial = False
        reset = False
        ret = check_reset_button(ip_add)

    if module == "M":
        secs = 3
        ret = pinguut(ip_add, secs)



    print(ret)

if __name__ == '__main__':
    main()