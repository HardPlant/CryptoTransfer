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
        self.host = host
        self.port = port

    def run(self):
        pass

    def boot(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        conn, addr = s.accept()
        print('Connected by', addr)

        self.echo(conn,addr)
        conn.close()

    def stop(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.host))
        s.send('')
        data = s.recv(1024)
        s.close()
        return self.server.join()

    def echo(self,conn,addr):
        running = True
        while running is True:
            data = conn.recv(1024)
            if not data: break
            conn.send(data)







