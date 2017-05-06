import os

from OLD_Files import GetOS as gos


def PingUUT(ip_add, secs):

    pingcount = 0

    while True:
        print("pinging UUT at ip " + ip_add +' count ' +  str(pingcount))
        if gos.get_platform =='Linux':
            data = ('ping '+ ip_add + ' -w 1000 -c 1')  # set ping timeout to 1000ms
        else:
            data = ('ping '+ ip_add + ' -w 1000 -n 1')
        response = os.system(data)              #default ping takes 3 secs to respond
        print(response)
        if response == 0:
            print(ip_add + ' is up!')
            return True, ip_add + ' is up!'
        else:
            print(ip_add + ' is down!')
            pingcount = pingcount + 1
            if pingcount > secs:
                return False, ip_add + ' is down!'


def __init__(self):
    super().__init__()
    self.initUI()

def main():
    ip_add = '192.168.1.99'
    ret = PingUUT(ip_add,3)
    print(ret)

if __name__ == '__main__':
    main()

