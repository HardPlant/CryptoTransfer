# Echo server program
import socket
import threading
import queue
# from CustomCrypto.mode import ECB
import CustomCrypto.LEA as LEA


def get_encryptor():
    return LEA.ECB(True, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)


def response(request):
    encryptor = get_encryptor()
    encrypt = encryptor.encrypt(request)
    final = encryptor.final()
    return encrypt+final


class EchoServer(threading.Thread):
    def __init__(self, host='127.0.0.1', port=50007):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.connector = queue.Queue()
        self._stop_event = threading.Event()

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
            print("Server stopped.")
            self.s.close()


    def stopped(self):
        if self._stop_event.is_set():
            print("Thread stop checked")
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

        print("Listen() Stopped")
        self.sock.close()
        return True

    def listenToClient(self, client, address):
        res = b''
        while not self.stopped():
            try:
                data = client.recv(1024)
                if data:
                    res = response(data)
                    print('Server sends:')
                    print(res)
                    client.send(res)
                else:
                    print("disconnected within else :" + str(address[0]) + ':' + str(address[1]))
                    print(res)
                    raise Exception('Client disconnected')
            except:
                print("disconnected with Exception:" + str(address[0]) + ':' + str(address[1]))
                client.close()
                return False

        if client:
            print("listenToClient() Stopped")
            client.close()
            return True
