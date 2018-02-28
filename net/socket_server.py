import socket
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)
print "Waitting for connection..."

def tcplink(sock, addr):
    print "Accept new connect from %s:%s.." % addr
    sock.send('welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            print 'exit'
            break
        sock.send('Hello, %s' % data)
    sock.close()

while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
