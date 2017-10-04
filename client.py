# Echo client program
import socket
import threading
import CustomCrypto.LEA as LEA
import queue

def get_decryptor():
    return LEA.ECB(False, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)

class Client():
    def __init__(self, host = '127.0.0.1', port = 50007):
        self.host = host
        self.port = port
        self.resp = queue.Queue()
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
            decryptor = get_decryptor()
            s = self.s
            if type(data) is str:
                data = bytes(data,'utf-8')
            s.send(data)
            data = s.recv(1024)
            data = decryptor.decrypt(data) + decryptor.final()
            print('Received', repr(data))
            self.resp.put(data)
        except:
            self.s.close()
            print("Client: remote connection failed")

