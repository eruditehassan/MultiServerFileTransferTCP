import socket
import sys, os
from threading import Thread

host = "127.0.0.1"
port = 12700
server_id = 0


class Server(Thread):

    def __init__(self,host,port_in):
        global server_id
        global port
        Thread.__init__(self)
        self.port = port_in
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host,port_in))
        server_id += 1
        self.id = server_id
        port += 1

    def run(self):
        print("Server ", self.id, " is operational")


threads = []

for _ in range(3):
    newthread = Server(host, port)
    newthread.daemon = True
    newthread.start()
    threads.append(newthread)


for t in threads:
    t.join()

print("Message sent successfully")