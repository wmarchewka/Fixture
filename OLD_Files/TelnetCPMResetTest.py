import os
import time

from OLD_Files import GetOS as gos


def PingUUT(ip_add):
    global respond_initial
    print("pinging UUT at ip " + ip_add)
    if gos.get_platform =='Linux':
        data = ('ping '+ ip_add + ' -w 1000 -c 1')  # set ping timeout to 1000ms
    else:
        data = ('ping '+ ip_add + ' -w 1000 -n 1')
    response = os.system(data)              #default ping takes 3 secs to respond IF UNAVAILABLE
    if response == 0:
        return True
    else:
        return False

def check_reset_button(ip_add):
    global respond_initial
    global reset
    while  True:
        val = PingUUT(ip_add)
        if val:
            respond_initial = True
            print('press reset button')
            time.sleep(2)
        if respond_initial == False:
            print('did not respond to initial ping')
            return False,  'Did not respond to initial ping'
        if respond_initial == True and val ==  False:
            print ('Unit resetting...')
            reset = True
        if  val == True and reset == True:
             print("Successfully reset...")
             return True, "Successfully reset..."

def __init__(self):
    super().__init__()
    self.initUI()

def main():
    global respond_initial
    global reset
    respond_initial = False
    reset = False
    ip_add = '192.168.1.6'
    ret = check_reset_button(ip_add)
    print(ret)

if __name__ == '__main__':
    main()