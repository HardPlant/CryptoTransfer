# Echo server program
import socket
import threading
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
        self._stop_event = threading.Event()

    def run(self):
        self.listen()

    def stop(self):
        print("Server try to stop")
        self._stop_event.set()

    def stopped(self):
        if self._stop_event.is_set():
            print("Thread stop checked")
        return self._stop_event.is_set()

    def listen(self):
        print('Server running at ' + self.host + ':' + str(self.port))
        self.sock.listen(5)
        while not self.stopped():
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient, args=(client, address)).start()

        print("Listen() Stopped")
        self.sock.close()

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
                    print("disconnected with Response:")
                    print(res)
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False

        if client:
            print("listenToClient() Stopped")
            client.close()
