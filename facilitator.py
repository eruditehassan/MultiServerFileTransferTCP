from socket import *
import _thread
import os

host_ip = "127.0.0.1"
port = 12700
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((host_ip, port))
sock.listen(5)
print("Waiting for connections")


# connection,add5ress = sock.accept()
# data = sock.recv(1073741824)
data = 0
server_count = 0
total_bytes = 0



def serve(clientsocket,addr):
    global data
    global server_count
    global total_bytes
    client_ip, client_port = clientsocket.getsockname()
    server_id = clientsocket.recv(1024).decode("utf-8")
    print("connected to {}".format(server_id))
    server_count +=1
    clientsocket.send(str(server_count).encode('utf-8'))
    #data = clientsocket.recv(104857600*2)
    filepath = "file_recv/part000{}".format(server_id)
    file = open(filepath, 'wb')

    data = clientsocket.recv(1024)
    total_bytes += 1024
    while (data):
        file.write(data)
        data = clientsocket.recv(1024)
        total_bytes += 1024
    file.close()
    join("file_recv", "file_join.mp4")

readsize = 1024

def join(fromdir, tofile):
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    parts.sort(  )
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(1024)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close(  )
    output.close(  )


while True:
    clientsocket, addr = sock.accept()

    _thread.start_new_thread(serve, (clientsocket, addr))







