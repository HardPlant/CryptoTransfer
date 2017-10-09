# Echo client program
import socket
import threading
import CustomCrypto.LEA as LEA
import queue

def get_encryptor():
    return LEA.ECB(LEA.ENCRYPT_MODE, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)

def get_ECB_encryptor(key):
    return LEA.ECB(LEA.ENCRYPT_MODE, key)

def get_CTR_encryptor(key):
    return LEA.CTR(LEA.ENCRYPT_MODE,key, '0123456701234567')

class Client():
    def __init__(self, host = '127.0.0.1', port = 50007, mode = 'ECB'):
        self.host = host
        self.port = port
        self.resp = queue.Queue()
        self.mode = mode
        print("Sender Running..")

    def send(self,data):
        thread = threading.Thread(target=self.sendsocket, args=(self.host,self.port,data,self.resp))
        thread.daemon = True
        thread.start()
        thread.join()
        if not self.resp.empty():
            data = self.resp.get()
        else:
            data = None
        self.s.close()
        return data

    def sendsocket(self,host, port, data,queue):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, port))
            encryptor = get_encryptor()
            s = self.s
            if type(data) is str:
                data = bytes(data,'utf-8')
            data = encryptor.update(data) + encryptor.final()
            s.send(data)
            data = s.recv(1024)
            print('Received', repr(data))
            self.resp.put(data)
        except:
            self.s.close()
            print("Client: remote connection failed")

