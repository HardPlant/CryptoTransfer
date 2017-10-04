# Echo client program
import socket

class EchoClient(object):
    def __init__(self, host = '', port = 50007):
        self.setUp(host,port)

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





