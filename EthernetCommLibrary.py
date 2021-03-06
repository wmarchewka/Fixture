import base64
import os
import socket
import telnetlib
import time
import requests

import FileConfigurationLibrary as fl
import SupportLibrary as sl
import logging


# TODO make sure to come up with a way to get ip address from config file
# TODO make sure all exception hndling is done and the same
# TODO make sure all testing and data log is the same
# TODO create the foollowing routines:
# 1. set UCR ( set to 0)
# 2.


logger = logging.getLogger()


#***************************************************************************************************************
class EthComLib(object):
    def __init__(self, osname):
        logger.debug('EthComLib class is initializing')
        self.osname = sl.supportLibrary.getOsPlatform(self)



# ******************************************************************************************
    def waittest(self):
        timecounter = 0
        while timecounter < 10:
            time.sleep(1)
            timecounter = timecounter + 1
            self.lblStatus.setText('Time counter ' + str(timecounter))
        return True, timecounter

    # ******************************************************************************************
    def pinguut(self, allow_msg, ip_address, numpings=1):
        pingcount = 1

        while True:
            logger.debug("pinging UUT at ip " + ip_address + ' count ' + str(pingcount))
            if allow_msg:
                self.lblStatus.setText("pinging UUT at ip " + ip_address + ' count ' + str(pingcount))
            os_platform = sl.supportLibrary.getOsPlatform(self)
            if os_platform == 'Linux':
                data = ('ping ' + ip_address + ' -w 1000 -c 1')  # set ping timeout to 1000ms
            elif os_platform == 'Windows':
                data = ('ping ' + ip_address + ' -w 1000 -n 1')
            elif os_platform == 'OSX':
                data = ('ping ' + ip_address + ' -W 1000 -c 1')
            response = os.system(data)  # default ping takes 3 secs to respond
            logger.debug('Response->' + str(response))
            logger.debug(response)
            if int(response) == 0:
                logger.debug(ip_address + ' is up!')
                if allow_msg:
                    self.lblStatus.setText(ip_address + ' is up!')
                return True, ip_address + ' is up!'
            else:
                logger.debug(ip_address + ' is down!')
                if allow_msg:
                    self.lblStatus.setText(ip_address + ' is down!')
                pingcount = pingcount + 1
                if pingcount > numpings:
                    return False, ip_address + ' is down!'
    # ******************************************************************************************
    def rebootunit_check(self, ip_address):

        timecounter = 0

        try:
            host = ip_address
            port = 23
            logger.debug('Rebooting unit ' + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = host, port
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$reboot\r\n')
            data = sc.recv(100)
            logger.debug(data)
            if str(data).find('OK') > -1:
                logger.debug("Reboot command accepted please wait.")
                self.lblStatus.setText('Reboot command accepted please wait.')
                time.sleep(5)
                while True:
                    val = EthComLib.pinguut(self, ip_address, 1)
                    logger.debug('val->' + str(val))
                    if val[0] == True:
                        logger.debug("Successfully reset...")
                        update = ('Successfully reset...')
                        self.lblStatus.setText(update)
                        return True, "Successfully reset..."
                    else:
                        timecounter = timecounter + 1
                        logger.debug('Waiting for unit to respond ' + str(timecounter) + ' seconds')
                        update = ('Waiting for unit to respond ' + str(timecounter) + ' seconds')
                        self.lblStatus.setText(update)
                        time.sleep(1.0)
                        if timecounter > 10:
                            logger.debug('Timeout waiting for unit to respond...')
                            update = ('Timeout waiting for unit to respond...')
                            self.lblStatus.setText(update)
                            return False, 'Timeout waiting for unit to respond...'

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err


        except Exception as err:
            logger.debug(err)
            return False, err  # 'Unit did not respond to reboot command...'

    # ******************************************************************************************
    def reset_button_check(self, ip_address):
        update = ''
        timecounter = 0
        respond_initial = False
        reset = False

        while True:
            val = EthComLib.pinguut(self, ip_address, 1)
            logger.debug('val->' + str(val))
            if val[0] == True and reset == True:
                logger.debug("Successfully reset...")
                update = ('Successfully reset...')
                self.lblStatus.setText(update)
                return True, "Successfully reset..."
            if val[0] == True:
                timecounter = timecounter + 1
                respond_initial = True
                logger.debug('Press reset button. Waiting ' + str(timecounter) + ' seconds')
                update = ('Press reset button.  Waiting ' + str(timecounter) + ' seconds')
                self.lblStatus.setText(update)
                time.sleep(1.0)
                if timecounter == 5:
                    logger.debug('Timedout waiting for button press...')
                    update = ('Timed out waiting for button press...')
                    self.lblStatus.setText(update)
                    return False, 'Timed out waiting for button press'
            if not respond_initial:
                logger.debug('Did not respond to initial ping...')
                update = ('Did not respond to initial ping...')
                return False, 'Did not respond to initial ping'
            if respond_initial == True and val[0] == False:
                logger.debug('Unit resetting...')
                update = ('Unit resetting...')
                reset = True
            logger.debug('respond initial->' + str(respond_initial))
            logger.debug('')
            self.lblStatus.setText(update)

    # ******************************************************************************************
    def lan_mac_write(self, ip_address):
        try:
            host = ip_address
            port = 23
            logger.debug('Setting LAN MAC address on ' + host)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = host, port
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            sc.write(b'$lanmac,G\r\n')
            old_mac = sc.recv(100)
            old_mac = old_mac.decode().split(',')[2]
            logger.debug('old_mac -> ' + old_mac)
            old_mac = str(old_mac)
            new_mac = old_mac
            logger.debug('new_mac -> ' + new_mac)
            self.lblStatus.setText('Old MAC : ' + str(old_mac) + '     New MAC : ' + str(new_mac))
            se = '$lanmac,S,' + new_mac + str('\r\n')
            sc.write(se.encode())
            data = sc.recv(100)
            logger.debug('data->' + str(data))
            result = data.decode().split(',')[3].find('OK')
            logger.debug('result->' + str(result))
            if result > 0:
                logger.debug('Lan Mac not set')
                return False, "Lan Mac not set"
                self.lblStatus.setText('Lan MAC not set')
            else:
                logger.debug('Lan Mac successfully set')
                return True, 'Lan Mac successfully set'
                self.lblStatus.setText('Lan MAC successfully set')

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

# ******************************************************************************************
    def frequency_read(self, allow_msg, ip_address):
        try:
            logger.debug("Getting Frequency from " + ip_address)
            if allow_msg:
                self.lblStatus.setText("Getting Frequency from " + ip_address)
            tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = ip_address, 23
            tn.settimeout(4)
            tn.connect(conn)
            tn.send(b"\n")
            tempdata = tn.recv(100)
            tn.send(b"$login,factory,factory\n")
            tempdata = tn.recv(50)
            logger.debug(str(tempdata))
            tn.send(b"$mdra,0,U0018\n")  # use this to see if a slip error returns
            tempdata = tn.recv(100)
            logger.debug(str(tempdata))
            slip_err = tempdata.find(b'SLIP_DRIVER_ERROR_READ_TIMEOUT')
            tempdata = ''
            if slip_err >= 0:
                logger.debug('SLIP driver error')
                return False, 'FAIL \n Failed to get voltages. \n  SLIP Driver Error'
            else:
                tn.close()
                PORT = 23
                TIMEOUT = 5
                tn = telnetlib.Telnet(host=ip_address, port=PORT, timeout=TIMEOUT)
                tn.write(b'$login,factory,factory\n')
                tn.write(b"$freq\n\r")
                tempdata = tn.read_all()
                logger.debug(tempdata)
                tn.close()
                tempdata = str(tempdata)
                tempdata = tempdata.split(',')
                logger.debug(tempdata)
                Frequency = float(tempdata[3])
                logger.debug(Frequency)
                return True, Frequency
        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

# ******************************************************************************************
    def voltage_read(self, ip_address):
        try:
            logger.debug("Getting Voltages from " + ip_address)
            self.lblStatus.setText("Getting voltages from " + ip_address)
            tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = ip_address, 23
            tn.settimeout(4)
            tn.connect(conn)
            tn.send(b"\n")
            tempdata = tn.recv(100)
            tn.send(b"$login,factory,factory\n")
            tempdata = tn.recv(50)
            logger.debug(str(tempdata))
            tn.send(b"$mdra,0,U0018\n")  # use this to see if a slip error returns
            tempdata = tn.recv(100)
            logger.debug(str(tempdata))
            slip_err = tempdata.find(b'SLIP_DRIVER_ERROR_READ_TIMEOUT')
            tempdata = ''
            if slip_err >= 0:
                logger.debug('SLIP driver error')
                return False, 'FAIL \n Failed to get voltages. \n  SLIP Driver Error'
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
                logger.debug(tempdata)
                tn.close()
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
                #logger.debug(voltageA, voltageB, voltageC)
                #logger.debug(currentA, currentAneg, currentB, currentBneg, currentC, currentCneg)
                data1 = ("Voltages acquired from " + ip_address + '\tL1: ' + str(voltageA) + '\tL2: ' + str(
                    voltageB) + '\tL3: ' + str(voltageC))
                logger.debug(data1)
                data2 = ('Currents acquired from ' + ip_address + '\tL1: ' + str(currentA) + '\tL2: ' + str(
                    currentB) + '\tL3: ' + str(currentC) + '\tL1_Neg:' + str(currentAneg) +    '\tL2_Neg:' + str(currentBneg)
                        + '\tL3_Neg:' + str(currentCneg) )
                logger.debug(data2)
                return True, voltageA, voltageB, voltageC, currentA, currentAneg, currentB, currentBneg, currentC, currentCneg

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err



# ******************************************************************************************

    def m40_buttontest(self, ip_address):
        try:

            port = 23
            logger.debug('Starting button test on ' + ip_address)
            self.lblStatus.setText('Starting button test on ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = ip_address, port
            PORT = 23
            TIMEOUT = 5
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            # tn = telnetlib.Telnet(host=HOST, port=PORT, timeout=TIMEOUT)
            # tn.write(b'$login,factory,factory\n')
            # tn.write(b"$bts,s,0\n")
            # tn.write(b"$bts,G\n\r")
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$bts,s,0\r\n')
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$bts,G\r\n')
            data = sc.recv(100)
            logger.debug(data)
            t = 0
            p = ''
            while True:
                sc.send(b'$bts,G\r\n')
                data = sc.recv(100)
                logger.debug(data)
                time.sleep(1)
                t = t + 1
                logger.debug('t ' + str(t))
                if t == 25:
                    logger.debug("User failed to start button test")
                    return False, "User failed to start button test"
                d = str(data).split(',')
                d = d[2]
                if p != d:
                    t = 0
                p = d
                logger.debug(d.encode('ascii'))
                if d == '1':
                    logger.debug('Press Button 1')
                    self.lblStatus.setText('Press Button 1.  ' + str(24 - t) + ' seconds remain')
                    r = 1
                if d == '2':
                    logger.debug('press button 2')
                    self.lblStatus.setText('Press Button 2')
                    self.lblStatus.setText('Press Button 1.  ' + str(24 - t) + ' seconds remain')

                if d == '3':
                    logger.debug('press button 3')
                    self.lblStatus.setText('Press Button 3')
                    self.lblStatus.setText('Press Button 1.  ' + str(24 - t) + ' seconds remain')

                if d == '4':
                    logger.debug('press button 4')
                    self.lblStatus.setText('Press Button 4')
                    self.lblStatus.setText('Press Button 1.  ' + str(24 - t) + ' seconds remain')

                if d == '5':
                    logger.debug('Unit passed button test')
                    self.lblStatus.setText('Unit passed button test')
                    self.lblStatus.setText('Press Button 1.  ' + str(25 - t) + ' seconds remain')

                    sc.close
                    return True, "Unit passed Button Test"
            logger.debug("timeout")
            sc.close()
            False, "Timeout"

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err
    # ******************************************************************************************
    def modbus_init(self, ip_address):

        self.lblStatus.setText('Writing Modbus settings')

        try:
            # TODO need to finsih this
            # logger.debug("Setting modbus defaults")
            PORT = 23
            TIMEOUT = 5
            # self.lblStatus.setText('Writing Modbus settings')
            tn = telnetlib.Telnet(host=ip_address, port=PORT, timeout=TIMEOUT)
            modbus_baudrate = fl.configfileRead('MODBUS', 'baud_rate')
            modbus_parity = fl.configfileRead('MODBUS', 'parity')
            modbus_stopbits = fl.configfileRead('MODBUS', 'stop_bits')
            if modbus_parity == 'EVEN':
                parity = '0'
            if modbus_parity == 'ODD':
                parity = '1'
            if modbus_parity == 'NONE':
                parity = '2'
            tn.write(b'$login,factory,factory\n')
            tn.write(b'$modbd,s,' + modbus_baudrate.encode('utf-8') + b'\n')
            tn.write(b'$modp,s,' + parity.encode('utf-8') + b'\n')
            tn.write(b'$modst,s,' + modbus_stopbits.encode('utf-8') + b'\n')
            tn.write(b'\r')
            tempdata = tn.read_all().decode('ascii')
            logger.debug(tempdata)
            tn.close()
            time.sleep(3)
            rebootreturn = EthComLib.rebootunit_check(self, ip_address)
            # TODO this shout be reboot test !
            pingreturn = EthComLib.pinguut(self, ip_address, 5)
            if rebootreturn:
                return True, 'Modbus successfully initialized...'
            else:
                return False, 'Unit failed to return from reboot'


        except TimeoutError as err:
            logger.debug(err)
            return False, err

        except Exception as err:
            logger.debug(err)
            return False, err

        except OSError as err:
            logger.debug(err)
            return False, err

        except IOError as err:
            logger.debug(err)
            return False, err

        except ValueError as err:
            logger.debug(err)
            return False, err

    # ******************************************************************************************
    def pcr_write(self, ip_address):
        try:
            logger.debug("Setting PCR value on " + ip_address)
            self.lblStatus.setText('Setting PCR value on ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = 23
            conn = ip_address, port
            sc.settimeout(2)
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$PCR,S,E0100110\r\n')
            data = sc.recv(100)
            logger.debug('data -> ' + str(data))
            data = data.decode().split(',')[3].find('OK')
            sc.close()
            if data > 0:
                logger.debug('PCR not set')
                self.lblStatus.setText('PCR not set' + ip_address)
                return False, "PCR not set"

            else:
                logger.debug('PCR successfully set')
                self.lblStatus.setText('PCR successfully set')
                return True, 'PCR successfully set'

        except socket.timeout as err:
            logger.debug('socket timeout')
            return False, err

        except socket.error as err:
            logger.debug('socket error')
            return False, err

        except OSError as err:
            sc.close
            logger.debug(err)
            return False, err

    # ******************************************************************************************
    def serialnumber_write(self, ip_address, serialnumber):
        try:
            # TODO this needs finished
            port = 23
            logger.debug('Writing serial number ' + str(serialnumber) + ' to ' + ip_address)
            self.lblStatus.setText('Writing serial number ' + str(serialnumber) + ' to ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = ip_address, port
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            senddata = '$pserial,S,' + str(serialnumber) + '\r\n'
            logger.debug('senddata-> ' + senddata)
            sc.send(senddata.encode('utf-8'))
            data = sc.recv(100)
            sc.close()
            logger.debug(data.decode().split(',')[2].find('OK'))
            if data.decode().split(',')[2].find('OK'):
                logger.debug('Device Serial number set to ' + str(serialnumber))
                self.lblStatus.setText('Device Serial number set to ' + str(serialnumber))
                return True, serialnumber
            else:
                logger.debug('Device Serial not set')
                self.lblStatus.setText("Device Serial not set")
                return False, "Device Serial not set"

        except TimeoutError as err:
            logger.debug(err)
            return False, err

        except Exception as err:
            logger.debug(err)
            return False, err

        except OSError as err:
            logger.debug(err)
            return False, err

    # ******************************************************************************************
    def serialnumber_read(self, ip_address):
        try:
            # TODO this needs finished
            port = 23
            logger.debug('Reading serial number from ' + ip_address)
            self.lblStatus.setText('Reading serial number from ' + ip_address)

            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(3)
            conn = ip_address, port
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            data = ''
            sc.send(b'$pserial,G\r\n')
            data = sc.recv(100)
            result = data.decode().split(',')[3].find('OK')
            serialnumber = data.decode().split(',')[2]
            logger.debug('return data->' + str(data))
            if result:
                logger.debug('Error retrieving device serial number...')
                return False, 'Error retrieving device serial number'
            else:
                logger.debug('Device serial ' + str(serialnumber))
                return True, serialnumber

        except TimeoutError as err:
            logger.debug(err)
            return False, err

        except Exception as err:
            logger.debug(err)
            return False, str(err) + ' retreiving serial number...'

        except OSError as err:
            logger.debug(err)
            return False, err

    # ******************************************************************************************
    def defaults_store(self, ip_address):

        try:
            port = 23
            logger.debug('Storing default values on ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(1)
            conn = ip_address, port
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$pgd\r\n')
            result = b''
            buf = sc.recv(4096)
            logger.debug(len(buf))
            result += buf
            logger.debug('received -> ' + str(buf))
            try:
                while buf:
                    buf = sc.recv(1024)
                    if not buf:
                        break
                    result += buf
                    logger.debug(buf)
            except OSError as err:
                logger.debug(err)
                if err and len(str(buf)) > 0:
                    result = result.decode().find('OK')
                    logger.debug('result->' + str(result))
                    if result > 0:
                        logger.debug('Defaults stored...')
                        self.lblStatus.setText('Defaults stored...')
                        return False, 'Defaults stored...'
                    else:
                        logger.debug('Defaults not stored...')
                        self.lblStatus.setText('Defaults not stored...')
                        return True, 'Defaults not stored...'
                else:
                    logger.debug('error')
        except Exception as err:
            logger.debug(err)
            return False, err

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

    # ******************************************************************************************
    def wifi_mac_write(self, ip_address, auto_inc, manual_mac):
        try:
            port = 23
            logger.debug('Setting wireless LAN MAC ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = ip_address, port
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            sc.send(b'$wlanmac,G\r\n')
            old_mac = sc.recv(100)
            old_mac = old_mac.decode().split(',')[2]
            logger.debug('old_mac -> ' + old_mac)
            old_mac = str(old_mac)
            if auto_inc:
                new_mac = EthComLib.get_next_mac(self)
                if new_mac[0]:
                    new_mac = new_mac[1]
                else:
                    return False, 'Out of Mac adresses.  Please call UEC'
            else:
                new_mac = manual_mac
            logger.debug('new_mac -> ' + new_mac)
            self.lblStatus.setText('Old MAC : ' + str(old_mac) + '     New MAC : ' + str(new_mac))
            se = '$wlanmac,S,' + new_mac + str('\r\n')
            sc.write(se.encode())
            data = sc.recv(100)
            logger.debug('data->' + str(data))
            result = data.decode().split(',')[3].find('OK')
            logger.debug('result->' + str(result))
            if result > 0:
                logger.debug('Wireless lan mac not set')
                self.lblStatus.setText('WIFI MAC not set')
                return False, "WIFI MAC not set"
            else:
                logger.debug('WIFI mac successfully set')
                self.lblStatus.setText('WIFI mac successfully set')
                return True, 'WIFI MAC successfully set'

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

    # ******************************************************************************************
    def get_next_mac(self):
        next_mac = fl.configfileRead('MAC_ADDRESS', 'next_mac')
        max_mac = fl.configfileRead('MAC_ADDRESS', 'max_mac')
        next_mac_parts = next_mac.split(':')
        max_mac_parts = max_mac.split(':')
        hex_next_mac = next_mac_parts[0] + next_mac_parts[1] + next_mac_parts[2]
        hex_next_mac = hex_next_mac + next_mac_parts[3] + next_mac_parts[4] + next_mac_parts[5]
        hex_max_mac = max_mac_parts[0] + next_mac_parts[1] + next_mac_parts[2]
        hex_max_mac = hex_max_mac + max_mac_parts[3] + next_mac_parts[4] + next_mac_parts[5]
        logger.debug('hex next mac ' + hex_next_mac)
        logger.debug('hex max mac ' + hex_max_mac)
        hex_next_mac = hex(int(hex_next_mac, 16) + 1)
        hex_max_mac = hex(int(hex_max_mac, 16))
        logger.debug('hex next mac ' + hex_next_mac)
        if hex_next_mac >= hex_max_mac:
            return False, "Out of Mac addresses"
        else:
            # hex_next_mac = hex(hex_next_mac)
            t = iter(hex_next_mac)
            x = ':'.join(a + b for a, b in zip(t, t))
            x = x[3:]
            logger.debug(x)
            fl.configfileWrite('MAC_ADDRESS', 'next_mac', x)
            return True, str(x)

    # ******************************************************************************************
    def file_size(fname):
        import os
        statinfo = os.stat(fname)
        return statinfo.st_size

    # ******************************************************************************************
    def fileupload(self, ip_address, slot):
        try:
            boardtype = fl.configfileRead('UUT', "major_board_type")
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
            # host = fl.configfileRead('TELNET',"ip_address")
            user = 'factory'
            password = 'factory'
            port = 80
            logger.debug('Starting uploading of file ' + path + ' to  ' + ip_address)
            self.lblStatus.setText('Starting uploading of file ' + path + ' to  ' + ip_address)

            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(1)
            conn = ip_address, port
            sc.connect(conn)

            fsize = EthComLib.file_size(path)
            filename = open(path, "br")
            fn = filename.read()

            myauthorization = base64.b64encode(user.encode('ascii') + b":" + password.encode('ascii'))

            my_req_body = "-----------------------------7dd3201c5104d4\r\n"
            my_req_body = my_req_body + 'Content-Disposition: form-data; name="' + str(slot) + '"; filename="' + str(
                path) + '"\r\n'
            my_req_body = my_req_body + 'Content-Type: application/octet-stream'
            my_req_body = my_req_body + '\r\n\r\n'
            my_req_end = "\r\n-----------------------------7dd3201c5104d4\r\n"

            logger.debug('Length of body->' + str(len(my_req_body)))
            logger.debug('Length of file->' + str(fsize))
            logger.debug('Length of end->' + str(len(my_req_end)))

            totalsize = len(my_req_body) + fsize + len(my_req_end)
            logger.debug('Total size->' + str(totalsize))

            my_req_head = "POST /upload_file.cgi HTTP/1.1\r\n"
            my_req_head = my_req_head + "Accept-Language: en-us\r\n"
            my_req_head = my_req_head + "Host: " + str(ip_address) + "\r\n"
            my_req_head = my_req_head + "Content-Type: multipart/form-data; boundary=---------------------------7dd3201c5104d4\r\n"
            my_req_head = my_req_head + "Content-Length: " + str(totalsize) + "\r\n"
            my_req_head = my_req_head + "Connection: Keep-Alive\r\n"
            my_req_head = my_req_head + "Authorization: Basic " + str(myauthorization, 'utf-8')  # ZmFjdG9yeTpmYWN0b3J5"
            my_req_head = my_req_head + "\r\n\r\n"
            my_req_head = my_req_head + "\r\n"

            # sys.stdout.write(my_req_head)
            # sys.stdout.write(my_req_body)
            # sys.stdout.buffer.write(fn)
            # sys.stdout.write(str(my_req_end))

            self.lblStatus.setText('Writing header info...')
            buffer = my_req_head.encode('ascii') + my_req_body.encode('ascii')
            while buffer:
                bytes = sc.write(buffer)
                buffer = buffer[bytes:]
            data = sc.recv(250)
            logger.debug('return data-------------------------')
            logger.debug(data)

            self.lblStatus.setText('Writing file info...')
            buffer = fn
            while buffer:
                bytes = sc.write(buffer)
                buffer = buffer[bytes:]
            data = sc.recv(1000)
            logger.debug('return data-------------------------')
            logger.debug(data)

            self.lblStatus.setText('Writing ending info...')
            buffer = my_req_end.encode('ascii')
            while buffer:
                bytes = sc.write(buffer)
                buffer = buffer[bytes:]
            data = sc.recv(500)
            logger.debug('return data-------------------------')
            # data = str(data)
            logger.debug(data)
            data = sc.recv(500)
            logger.debug('return data-------------------------')
            logger.debug(data)
            data = str(data)
            sc.close()
            if data.find('url=upload.html'):
                logger.debug('File upload successful')
                self.lblStatus.setText('File upload successful ')
            else:
                logger.debug('File upload failed')
                self.lblStatus.setText('File upload failed')

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

    # ******************************************************************************************
    def script_write(self, ip_address, path):
        try:
            port = 23
            logger.debug('Uploading script ' + path)
            self.lblStatus.setText('Uploading script ' + path)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(5)
            conn = ip_address, port
            script = open(path, 'br')
            fn = script.read()
            logger.debug('file-> ' + str(fn))
            sc.connect(conn)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug('login data>' + str(data))
            splitdata = fn.split(b'\r\n')
            logger.debug(splitdata)
            for linedata in splitdata:
                if linedata != b'':
                    sc.send(linedata + b'\r\n')
                    data = sc.recv(1000)
                    logger.debug('data->' + str(data))
            sc.close()
            self.lblStatus.setText('Uploading script successful')
            return True, 'Uploading script successful'


        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            self.lblStatus.setText('Uploading script failed. ' + str(err))
            return False, err

        except AttributeError as err:
            logger.debug(err)
            self.lblStatus.setText('Uploading script failed. ' + str(err))
            return False, err

# ******************************************************************************************
    def webpageversion_read(self, ip_address):

        try:
            # TODO this needs finished
            port = 80
            logger.debug('Checking Webpage version...')
            self.lblStatus.setText('Checking Webpage version...')

            r = requests.get('http://192.168.1.99/devinfo.html', timeout=1.000)
            logger.info(r.text)
            data = r.text
            founddata = data.find('Firmware Version:')
            if founddata != -1:
                version = data[founddata + 18:founddata + 34]
                logger.debug("Version->" + str(version))
                logger.debug("Found Data->" + str(founddata))

            if not data:
                self.lblStatus.setText('Webpage not installed.')
                return True, 'Webpage not installed'
            else:
                self.lblStatus.setText('Webpage version is ' + version)
                return True, 'Webpage version is ' + version

        except requests.exceptions.ConnectTimeout as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, 'Timeout connecting to UUT'


        except requests.exceptions.HTTPError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

    # ******************************************************************************************
    def wifiversion_read(self, ip_address):
        try:
            # TODO this needs finished
            port = 23
            logger.debug('Checking WIFI version...')
            self.lblStatus.setText('Checking WIFI version...')
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(3)
            conn = ip_address, port
            sc.connect(conn)
            sc.send(b'\r\n')
            data = sc.recv(100)
            sc.send(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug('login data-' + str(data))
            sc.send(b'$wv,g\r\n')
            data = sc.recv(100)
            logger.debug('recv data-' + str(data))
            data = data.decode().split(',')[2]
            logger.debug('return data->' + str(data))
            if not data:
                self.lblStatus.setText('WIFI not installed.')
                return True, 'WIFI not installed'
            else:
                self.lblStatus.setText('WIFI version is ' + str(data))
                return True, 'WIFI version is ' + str(data)

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

    # ******************************************************************************************
    def wifi_setup(self, ip_address):
        try:
            # TODO enusre this is able to set wifi ssid and other things needed
            # 1. ensure wlan mac address is set
            # 2. check wifi version  $wv
            # 3. set $wlanprg to 1 to accept the new file upload
            # 4. use file upload to upload the new version
            # 5. reboot
            # 6. check version again make sure equal to 0x00000000.
            # 7. reboot.


            # port = 23
            logger.debug('Starting WIFI Configuration ' + ip_address)
            self.lblStatus.setText('Starting WIFI Configuration ' + ip_address)
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(2)
            conn = ip_address, port
            sc.connect(conn)
            data = sc.recv(100)
            logger.debug(data)
            sc.write(b'$login,factory,factory\r\n')
            data = sc.recv(100)
            logger.debug(data)
            sc.write(b'$wlanmac,G\r\n')
            old_mac = sc.recv(100)
            old_mac = old_mac.decode().split(',')[2]
            old_mac = str(old_mac)
            if old_mac == 'N/A':
                logger.debug('No WIFI MAC Found')
                self.lblStatus.setText('No WIFI MAC found')
                return False, "No WIFI MAC found"
            else:
                logger.debug("Current MAC " + old_mac)
            if new_mac:
                logger.debug('old_mac -> ' + str(old_mac))
                logger.debug('new_mac -> ' + new_mac)
                logger.debug('Setting new mac address...')
                self.lblStatus.setText('Setting new mac address to ' + str(new_mac))
                se = '$wlanmac,S,' + new_mac + str('\r\n')
                sc.write(se.encode())
                data = sc.recv(100)
                logger.debug('data->' + str(data))
                result = data.decode().split(',')[3].find('OK')
                logger.debug('result->' + str(result))
                if result > 0:
                    logger.debug('Lan Mac not set')
                    self.lblStatus.setText("Lan Mac not set")
                    return False, "Lan Mac not set"
                else:
                    logger.debug('Lan Mac successfully set')
                    self.lblStatus.setText("Lan Mac successfully set")
                    ret = EthComLib.fileupload(self, 'wifi')
                    logger.debug(ret)

        except ConnectionError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except TimeoutError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except OSError as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err

        except Exception as err:
            logger.debug(err)
            logger.debug(type(err))
            return False, err


# ******************************************************************************************
def main():
    ip_add = '192.168.1.99'
    mac_add = '58:2f:42:20:00:01'
    path = r'C:\UEC\Functional Test\M50\Wi Fi No MB Default Script 062215.txt'
    module = 'A'

    if module == "A":
        ret = EthComLib.wifi_setup(ip_add, mac_add)

    if module == "B":
        ret = EthComLib.wifiversion_read(ip_add)

    if module == "C":
        ret = EthComLib.script_write(ip_add, path)

    if module == "D":
        global osname
        slot = 'web'
        logger.debug(osname)
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
        ret = EthComLib.m40_buttontest()

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

    logger.debug(ret)


if __name__ == '__main__':
    main()
