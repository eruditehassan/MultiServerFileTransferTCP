from socket import *
sock = socket(AF_INET,SOCK_STREAM)
serverIP = "127.0.0.1"
port = 12700
sock.connect((serverIP,port))
print("Connecting to server")
msg = "client"
sock.send(msg.encode("utf-8"))
data = sock.recv(1024)
print("Data received from facilitator {}".format(data.decode("utf-8")))
#print("Data received successfully!")