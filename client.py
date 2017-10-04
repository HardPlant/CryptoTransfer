# Echo client program
import socket
import threading
import CustomCrypto.LEA as LEA


decryptor = LEA.ECB(False, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)


class Client(threading.Thread):
    def __init__(self, host = '127.0.0.1', port = 50007):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        print("Sender Running..")

    def send(self,data):
        s = self.s
        self.s.connect((self.host, self.port))
        if type(data) is str:
            data = bytes(data,'utf-8')
        s.send(data)
        data = s.recv(1024)
        data = decryptor.decrypt(data) + decryptor.final()
        print('Received', repr(data))
        self.s.close()
        return data
