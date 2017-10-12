# Echo client program
import socket
import threading
import CustomCrypto.LEA as LEA
from CustomCrypto.LEA.MAC import getMAC
import queue

def get_encryptor(key, mode = 'ECB'):
    if mode == 'ECB':
        return get_ECB_encryptor(key)
    elif mode == 'CTR':
        return get_CTR_encryptor(key)

def get_ECB_encryptor(key):
    return LEA.ECB(LEA.ENCRYPT_MODE, key, PKCS5Padding=True)

def get_CTR_encryptor(key):
    return LEA.CTR(LEA.ENCRYPT_MODE, key, '0123456701234567')

class Client():
    def __init__(self, host = '127.0.0.1', port = 50007, mode = 'ECB', key = bytes('A',encoding='utf-8')*32):
        self.host = host
        self.port = port
        self.resp = queue.Queue()
        self.key = key
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

    def request(self, msg):
        try:
            encryptor = get_encryptor(self.key, self.mode)
            data = encryptor.update(msg) + encryptor.final()
            mac = getMAC(data, self.key)
            print('[Client] data :' + str(data))
            print('[Client] MAC :' + str(mac))
            return data + mac

        except Exception as e:
            print(e)

    def sendsocket(self,host, port, data,queue):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, port))
            s = self.s
            if type(data) is str:
                data = bytes(data,'utf-8')
            data = self.request(data)
            print('[Client] Sending :' + str(data))
            s.send(data)
            data = s.recv(1024)
            self.resp.put(data)
        except Exception as e:
            self.s.close()
            print(e)
            print("Client: remote connection failed")

