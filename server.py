# Echo server program
import socket
from multiprocessing import Process, Value
import CustomCrypto.mode.ECB
from CustomCrypto.LEA import LEA

class EchoServer(object):
    def __init__(self, host='127.0.0.1', port=50007):
        self.encryptor = LEA(bytes('AAAA') * 8)
        self.host = host
        self.port = port
        print("''Server Initialized")

    def getResponse(self,data):
        encrypt = self.encryptor.encrypt(data)
        return encrypt


    def boot(self,HOST,PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print('Connected by', addr)

        self.echo(conn,addr)
        conn.close()

    def start(self,host,port):
        self.server = Process(target=self.boot, args=(host,port))
        print("Server Started")
        while not self.server.is_alive():
            pass
        return True

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







