# Echo client program
import socket
from CustomCrypto.LEA import LEA

class EchoClient(object):
    def __init__(self, host = '127.0.0.1', port = 50007):
#        self.setUp(host,port)
        self.decrpytor = LEA(bytes('AAAA')*8)
        self.response = ''

    def request(self,data):
        return data

    def setUp(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def send(self):
        s = self.s
        s.send('Hello, world')
        data = s.recv(1024)
        print('Received', repr(data))
        return data

    def close(self):
        self.s.close()





