#coding:utf-8
#Author by Arice@Molecule Labs

import socket
import time
import sys
from listen import *

def Title():
    print 'python FL_client.py ip port dir'
    print 'ep:python FL_client.py 192.168.0.1 12345 /etc/'
    print 'The dir you want to monitor.'

def client(ip, port, directory):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
    except socket.error as msg:
        print msg
        sys.exit(1)
    print s.recv(1024)
    while 1:
        listen(directory,s).Run()
    s.close()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    client(sys.argv[1], sys.argv[2], sys.argv[3])