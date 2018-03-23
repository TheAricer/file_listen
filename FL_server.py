#coding:utf-8
#Author by Arice@Molecule Labs

import socket
import sys
import threading
import time

def Title():
    title ='''
  ___ _   _  ___  ___           
 / _ \ | | |/ _ \/ __|         
|  __/ |_| |  __/\__ \       
 \___|\__, |\___||___/          
      |___/                    
        Author by Arice@Molecule Labs
    '''
    print title
    print 'Usage : python FL_server.py ip port log'
    print 'Example : python FL_server.py 192.168.0.1 6666 /tmp/'
    print 'Warring: log need add //'

def server(ip, port, directory):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, int(port)))
        s.listen(2)
    except socket.error as msg:
        print msg
        sys.exit(1)
    print 'Success Waiting Connection...'

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=Thread_Run, args=(conn, addr, directory))
        t.start()

def file(Values, directory):
    dirr = directory + str(time.strftime('%Y%m%d',time.localtime(time.time()))) + '.log'
    f = open(dirr,'a')
    f.write(Values + '\n')


def Thread_Run(conn, addr, directory):
    NowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    conn_log = NowTime+ '--' + 'New connection from {0}'.format(addr)
    print conn_log
    conn.send('Server Connection Success')
    file(conn_log, directory)
    while 1:
        data = conn.recv(1024)
        if len(data) > 0:
            change_log = '{0} client send data：{1}'.format(addr, data)
            file(change_log, directory)
        else:
            break
    conn.close()

if __name__ == '__main__':
    Title()
    server(sys.argv[1], sys.argv[2],sys.argv[3]) 
