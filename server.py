# Echo server program
import socket
from multiprocessing import Process
import CustomCrypto.mode.ECB


class EchoServer(object):
    def __init__(self, host='', port=50007):
        self.host = host
        self.port = port
        self.server = Process(target=boot, args=(host,port))

    def start(self):
        return self.server.start()

    def stop(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.host))
        s.send('')
        data = s.recv(1024)
        s.close()
        return self.server.join()


running = True

def boot(HOST,PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)

    echo(conn,addr)
    conn.close()

def echo(conn,addr):
    while running is True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)
