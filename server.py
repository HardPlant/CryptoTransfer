# Echo server program
import socket
from multiprocessing import Process
import CustomCrypto.mode.ECB

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port

running = True
def boot():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print('Connected by', addr)
    conn, addr = s.accept()

    echo(conn,addr)
    conn.close()

def echo(conn,addr):
    while running is True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)
