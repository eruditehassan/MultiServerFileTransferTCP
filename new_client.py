import socket
import os

host_ip = "127.0.0.1"
port = 12700
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host_ip, port))
data = s.recv(1024)
print(data.decode('utf-8'))