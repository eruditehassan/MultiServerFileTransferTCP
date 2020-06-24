from socket import *
import sys, os

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(os.stat("file.mp4").st_size / 2) + 1

def split(fromfile, todir, chunksize=chunksize):
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fname in os.listdir(todir):            # delete any existing files
            os.remove(os.path.join(todir, fname))
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(todir, ('part%04d' % partnum))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum


split("file.mp4","file_out")

f = []
for (dirpath, dirnames, filenames) in os.walk("file_out"):
    f.extend(filenames)

sock = socket(AF_INET,SOCK_STREAM)
serverIP = "127.0.0.1"
port = 12700
sock.connect((serverIP,port))
print("Connecting to facilitator")


msg = "server 0"
# reading the
filename = "file_out/" + f[0]
file = open(filename,'rb')

#data = file.read(os.stat(filename).st_size)
sock.send(msg.encode("utf-8"))
server_id = sock.recv(1024)
server_id = int(server_id.decode('utf-8'))
print("Server ID is ",server_id)

data = file.read(1024)
while (data):
    sock.send(data)
    data = file.read(1024)

print("Data sent successfully!")


