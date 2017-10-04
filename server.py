# Echo server program
import socket
import threading
# from CustomCrypto.mode import ECB
import CustomCrypto.LEA as LEA


encryptor = LEA.ECB(True, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)


def response(request):
    encrypt = encryptor.encrypt(request)
    final = encryptor.final()
    return encrypt+final


class EchoServer(threading.Thread):
    def __init__(self, host='127.0.0.1', port=50007):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        self.boot()
        self.echo()
        self.conn.close()

    def boot(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        print('Server running at' + self.host + ':' + self.port)
        self.conn, self.addr = s.accept()
        print('Connected by', self.addr)

    def stop(self):
        stopper = threading.Thread(target=self.send_null())
        stopper.daemon = True
        stopper.start()

    def echo(self):
        running = True
        conn = self.conn
        addr = self.addr

        while running is True:
            data = conn.recv(1024)
            if not data: break
            res = response(data)
            conn.send(res)

    def send_null(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.host))
        s.send('')
        s.close()








