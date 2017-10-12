# Echo server program
import socket
import threading
import queue
import CustomCrypto.LEA as LEA
import traceback
from CustomCrypto.LEA.MAC import getMAC


def get_decryptor(key, mode = 'ECB'):
    if mode == 'ECB':
        return get_ECB_decryptor(key)
    elif mode == 'CTR':
        return get_CTR_decryptor(key)

def get_ECB_decryptor(key):
    return LEA.ECB(LEA.DECRYPT_MODE, key, PKCS5Padding=True)

def get_CTR_decryptor(key):
    return LEA.CTR(LEA.DECRYPT_MODE, key, '0123456701234567')



class EchoServer(threading.Thread):
    def __init__(self, host='127.0.0.1', port=50007, mode = 'ECB', key = bytes('A',encoding='utf-8')*32):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.key = key
        self.mode = mode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.connector = queue.Queue()
        self._stop_event = threading.Event()

    def validate(self, data):
        data_raw = data[:-16]
        data_mac = data[-16:]
        mac = getMAC(data_raw,self.key)
        print('[Server] MAC :' + str(mac))
        if data_mac == mac:
            return True
        else:
            return False


    def response(self, request):
        decryptor = get_decryptor(self.key, self.mode)
        decrypt = decryptor.update(request) + decryptor.final()
        return decrypt

    def run(self):
        self.listen()

    def stop(self):
        print("Server try to stop")
        self._stop_event.set()
        ct = threading.Thread(target = self.send_null, args=(self.host, self.port))
        ct.daemon = True
        ct.start()


    def send_null(self,host,port):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, port))
            self.s.send(b'')
        except:
            self.s.close()


    def stopped(self):
        if self._stop_event.is_set():
            pass
        return self._stop_event.is_set()

    def get_connector(self):
        if not self.connector.empty():
            result = self.connector.queue
            return result[-1]
        else:
            return None

    def listen(self):
        print('Server running at ' + self.host + ':' + str(self.port))
        self.sock.listen(1)
        while not self.stopped():
            client, address = self.sock.accept()
            self.connector.put(address)
            client.settimeout(60)
            ct = threading.Thread(target = self.listenToClient, args=(client, address))
            ct.daemon = True
            ct.start()

        self.sock.close()
        return True

    def listenToClient(self, client, address):
        res = b''
        while not self.stopped():
            try:
                data = client.recv(1024)
                if data:
                    print('[Server] incoming data :' + str(data))
                    data_raw = data[:-16]
                    if self.validate(data) :
                        res = self.response(data_raw)
                        print('[Server] Client says: ', end='')
                        print(res.decode())
                        client.send(res)
                    else:
                        print('[Server] Client MAC Failed: ', end='')
                        print(res.decode())
                        client.send("NAK")
                else:
                    # print("[Server] disconnected within else :" + str(address[0]) + ':' + str(address[1]))
                    # print(res)
                    raise Exception('Client disconnected')
            except Exception as e:
                client.close()
                return False

        if client:
            client.close()
            return True
