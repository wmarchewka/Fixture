import base64
import os
import socket
import telnetlib
import time

import FileConfigurationLibrary as fl
import SupportLibrary as sl

#TODO make sure to come up with a way to get ip address from config file
#TODO make sure all exception hndling is done and the same
#TODO make sure all testing and data log is the same

class EthComLib(object):

    def __init__(self):
        print('EthComLib class is initializing')
        osname = sl.supportLibrary.getOsPlatform(self)

    # ******************************************************************************************
    def waittest(self):
        time.sleep(10)

    #******************************************************************************************
    def pinguut(self, ip_address, numpings=1):
        pingcount = 0

        #ip_address = fl.configfileRead('TELNET', "ip_address")

        while True:
            print("pinging UUT at ip " + ip_address +' count ' +  str(pingcount))
            self.lblStatus.setText("pinging UUT at ip " + ip_address +' count ' +  str(pingcount))
            if sl.getOsPlatform() =='Linux':
                data = ('ping '+ ip_address + ' -w 1000 -c 1')  # set ping timeout to 1000ms
            elif sl.getOsPlatform() =='Windows':
                data = ('ping '+ ip_address + ' -w 1000 -n 1')
            elif sl.getOsPlatform() == 'OSX':
                data = ('ping ' + ip_address + ' -W 1000 -c 1')
            response = os.system(data)              #default ping takes 3 secs to respond
            print(response)
            if response == 0:
                print(ip_address + ' is up!')
                self.lblStatus.setText(ip_address + ' is up!')
                return True, ip_address + ' is up!'
            else:
                print(ip_address + ' is down!')
                self.lblStatus.setText(ip_address + ' is down!')
                pingcount = pingcount + 1
                if pingcount > numpings:
                    return False, ip_address + ' is down!'

    #******************************************************************************************
    def reset_button_check(self, ip_address):
        update = ''
        timecounter = 0
        respond_initial = False
        reset = False

        while  True:
            val = EthComLib.pinguut(self, ip_address, 1)
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
    def lan_mac_write(self, ip_address):
        try:
            host = ip_address
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
    def voltage_read(self, ip_address):
        try:
            print("Getting Voltages from " + ip_address)
            self.lblStatus.setText("Getting voltages from " + ip_address)
            tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = ip_address, 23
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
                tn = telnetlib.Telnet(host=ip_address, port=PORT, timeout=TIMEOUT)
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
                data =  ("Voltages acquired from " + ip_address + '\n\r' + 'L1: ' + str(voltageA) + '  L2: ' + str(voltageB) + '  L3: ' +str(voltageC))
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
    def m40_buttontest(self,ip_address):
        try:
            #host = "192.168.1.99"
            port = 23
            #HOST = '10.0.0.210'
            print('Starting button test on ' + ip_address)
            self.lblStatus.setText('Starting button test on ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = ip_address,port
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
    def modbus_init(self, ip_address):

        #TODO need to finsih this
        # print("Setting modbus defaults")
        PORT = 23
        TIMEOUT = 5
        self.lblStatus.setText('Writing Modbus settings')
        tn = telnetlib.Telnet(host=ip_address, port=PORT, timeout=TIMEOUT)
        tn.write(b'$login,factory,factory\n')
        tn.write(b'$modbd,s,19200\n')
        tn.write(b'$modp,s,1\n')
        tn.write(b'$modst,s,1\n')
        tn.write(b'$reboot\n')
        tn.write(b'\r')
        tempdata = tn.read_all().decode('ascii')
        print(tempdata)
        tn.close()
        return True,tempdata
    #******************************************************************************************
    def pcr_write(self, ip_address):
        try:
            print("Setting PCR value on " + ip_address)
            self.lblStatus.setText('Setting PCR value on ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = 23
            conn = ip_address, port
            sc.settimeout(2)
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            sc.send(b'$PCR,S,E0100110\r\n')
            data = sc.recv(100)
            print('data -> ' + str(data))
            data = data.decode().split(',')[3].find('OK')
            sc.close()
            if data > 0:
                print('PCR not set')
                self.lblStatus.setText('PCR not set' + host)
                return False, "PCR not set"

            else:
                print('PCR successfully set')
                self.lblStatus.setText('PCR successfully set')
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

    # ******************************************************************************************
    def serialnumber_write(self, ip_address, serialnumber):
        try:
            # TODO this needs finished
            port = 23
            print('Writing serial number '+ str(serialnumber) + ' to ' + ip_address)
            self.lblStatus.setText('Writing serial number ' + str(serialnumber) + ' to ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = ip_address, port
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            senddata = '$pserial,S,'+ str(serialnumber) + '\r\n'
            print('senddata-> '+ senddata)
            sc.send(senddata.encode('utf-8'))
            data = sc.recv(100)
            print(data.decode().split(',')[2].find('OK'))
            if data.decode().split(',')[2].find('OK'):
                print('Device Serial number set to ' + str(serialnumber))
                self.lblStatus.setText('Device Serial number set to ' + str(serialnumber))
                return True, serialnumber
            else:
                print('Device Serial not set')
                self.lblStatus.setText("Device Serial not set")
                return False, "Device Serial not set"


        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def serialnumber_read(self, ip_address):
        try:
            #TODO this needs finished
            port = 23
            print('Reading serial number from ' + ip_address)
            self.lblStatus.setText('Writing serial number from ' + ip_address)

            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(3)
            conn = ip_address, port
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            data=''
            sc.send(b'$pserial,G\r\n')
            data = sc.recv(100)
            result = data.decode().split(',')[3].find('OK')
            serialnumber = data.decode().split(',')[2]
            print('return data->' + str(data))
            if result:
                print('Device serial number not set...')
                return False, 'Device serial not set'
            else:
                print('Device serial ' +  str(serialnumber))
                return True, serialnumber

        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def defaults_store(self, ip_address):

        try:
            port = 23
            print('Storing default values on ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(1)
            conn = ip_address, port
            sc.connect(conn)
            data = sc.recv(100)
            print(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print(data)
            sc.send(b'$pgd\r\n')
            result = b''
            buf = sc.recv(4096)
            print(len(buf))
            result += buf
            print('received -> ' + str(buf))
            try:
                while buf:
                    buf = sc.recv(1024)
                    if not buf:
                        break
                    result += buf
                    print(buf)
            except OSError as err:
                print(err)
                if err and len(str(buf)) > 0:
                    result = result.decode().find('OK')
                    print('result->' + str(result))
                    if result > 0:
                        print('Defaults stored...')
                        self.lblStatus.setText('Defaults stored...')
                        return False, 'Defaults stored...'
                    else:
                        print('Defaults not stored...')
                        self.lblStatus.setText('Defaults not stored...')
                        return True, 'Defaults not stored...'
                else:
                    print('error')
        except Exception as err:
            print(err)
            return False, err



        #except OSError as err:
        #    print(err)
        #    return False, err

    #******************************************************************************************
    def wifi_mac_write(self, ip_address):
        try:
            port = 23
            print('Setting wireless LAN MAC ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = ip_address, port
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
            self.lblStatus.setText('Old MAC : ' + str(old_mac) + '     New MAC : ' + str(new_mac))
            se = '$wlanmac,S,' + new_mac + str('\r\n')
            sc.write(se.encode())
            data = sc.recv(100)
            print('data->' + str(data))
            result = data.decode().split(',')[3].find('OK')
            print('result->' + str(result))
            if result > 0:
                print('Wireless lan mac not set')
                self.lblStatus.setText('WIFI MAC not set')
                return False, "WIFI MAC not set"
            else:
                print('WIFI mac successfully set')
                self.lblStatus.setText('WIFI mac successfully set')
                return True, 'WIFI MAC successfully set'

        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def file_size(fname):
        import os
        statinfo = os.stat(fname)
        return statinfo.st_size

    #******************************************************************************************
    def fileupload(self, ip_address, slot):
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
            #host = fl.configfileRead('TELNET',"ip_address")
            user = 'factory'
            password = 'factory'
            port = 80
            print('Starting uploading of file ' + path + ' to  ' + ip_address)
            self.lblStatus.setText('Starting uploading of file ' + path + ' to  ' + ip_address)

            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(1)
            conn = ip_address, port
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
            my_req_head = my_req_head + "Host: " + str(ip_address) + "\r\n"
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

            self.lblStatus.setText('Writing header info...')
            buffer = my_req_head.encode('ascii') + my_req_body.encode('ascii')
            while buffer:
                bytes = sc.write(buffer)
                buffer = buffer[bytes:]
            data = sc.recv(250)
            print('return data-------------------------')
            print(data)

            self.lblStatus.setText('Writing file info...')
            buffer = fn
            while buffer:
                bytes = sc.write(buffer)
                buffer = buffer[bytes:]
            data = sc.recv(1000)
            print('return data-------------------------')
            print(data)

            self.lblStatus.setText('Writing ending info...')
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
                print('File upload successful')
                self.lblStatus.setText('File upload successful ')
            else:
                print('File upload failed')
                self.lblStatus.setText('File upload failed')

        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def script_write(self, ip_address, path):
        try:
            port = 23
            print('Uploading script ' + path)
            self.lblStatus.setText('Uploading script ' + path)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(5)
            conn = ip_address, port
            script = open(path,'br')
            fn = script.read()
            print('file-> ' + str(fn))
            sc.connect(conn)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print('login data>' + str(data))
            splitdata = fn.split(b'\r\n')
            print(splitdata)
            for linedata in splitdata:
                if linedata != b'':
                    sc.send(linedata + b'\r\n')
                    data = sc.recv(1000)
                    print('data->' + str(data))
            sc.close()
            self.lblStatus.setText('Uploading script successful')
            return True,'Uploading script successful'

        except OSError as err:
            print(err)
            self.lblStatus.setText('Uploading script failed. ' + str(err))
            return False, err

        except AttributeError as err:
            print(err)
            self.lblStatus.setText('Uploading script failed. ' + str(err))
            return False, err



    #******************************************************************************************
    def webpageversion_read(self, ip_address):
        try:
            #TODO this needs finished
            port = 23
            print('Checking webpage version...')
            self.lblStatus.setText('Checking webpage version...')
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(5)
            conn = ip_address, port
            sc.connect(conn)
            sc.send(b'\r\n')
            data = sc.recv(100)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            print('login data-' + str(data))
            sc.send(b'$wv,g\r\n')
            data = sc.recv(100)
            print('recv data-' + str(data))
            data = data.decode().split(',')[2]
            print('return data->' + str(data))
            if not data:
                self.lblStatus.setText('Webpage not installed.')
                return True, 'Webpage not installed'
            else:
                self.lblStatus.setText('Webpage version is ' + str(data))
                return True, 'Webpage version is ' + str(data)


        except OSError as err:
            print(err)
            return False, err

    #******************************************************************************************
    def wifi_setup(self, ip_address, new_mac):
        try:
            #TODO enusre this is able to set wifi ssid and other things needed
            port = 23
            print('Starting WIFI Configuration ' + ip_address)
            self.lblStatus.setText('Starting WIFI Configuration ' + ip_address)

            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = ip_address, port
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
                self.lblStatus.setText('No WIFI MAC found')
                return False, "No WIFI MAC found"
            else:
                print("Current MAC " + old_mac)
            if new_mac:
                print('old_mac -> ' + str(old_mac))
                print('new_mac -> ' + new_mac)
                print('Setting new mac address...')
                self.lblStatus.setText('Setting new mac address to ' + str(new_mac))
                se = '$wlanmac,S,' + new_mac + str('\r\n')
                sc.write(se.encode())
                data = sc.recv(100)
                print('data->' + str(data))
                result = data.decode().split(',')[3].find('OK')
                print('result->' + str(result))
                if result > 0:
                    print('Lan Mac not set')
                    self.lblStatus.setText("Lan Mac not set")
                    return False, "Lan Mac not set"
                else:
                    print('Lan Mac successfully set')
                    self.lblStatus.setText("Lan Mac successfully set")
                    ret = EthComLib.fileupload(self, 'wifi')
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
        ret = EthComLib.wifi_setup(ip_add, mac_add)

    if module == "B":
        ret = EthComLib.webpageversion_read(ip_add)

    if module == "C":
        ret = EthComLib.script_write(ip_add,path)

    if module == "D":
        global osname
        slot = 'web'
        print(osname)
        if osname == "Windows":
            path = r"C:\web_pages_UEC_AC_025_ENG.tfs"
        elif osname == "OS X":
            path = os.path.expanduser("~/web_pages_UEC025_ENG.tfs")
            ret = EthComLib.fileupload(slot)

    if module == "E":
        ret = EthComLib.wifi_mac_write(ip_add)

    if module == "F":
        ret = EthComLib.serialnumber_write(ip_add)

    if module == "G":
        ret = EthComLib.pcr_write(ip_add)

    if module == "H":
        ret = EthComLib.modbus_init(ip_add)

    if module == "I":
        ret  = EthComLib.m40_buttontest()

    if module == "J":
        ret = EthComLib.voltage_read()

    if module == "K":
        ret = EthComLib.lan_mac_write(ip_add)

    if module == "L":
        global respond_initial
        global reset
        respond_initial = False
        reset = False
        ret = EthComLib.reset_button_check(ip_add)

    if module == "M":
        secs = 3
        ret = EthComLib.pinguut(ip_add, secs)



    print(ret)

if __name__ == '__main__':
    main()