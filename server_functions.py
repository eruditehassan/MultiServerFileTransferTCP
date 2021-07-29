from socket import *
import os


def split(fromfile, todir,num_of_servers):
    """
    This function splits a file into n portions where n represents number 
    of servers. 
    """
    # Dividing file size by number of servers to get chunksize
    chunksize = int(os.stat("file.mp4").st_size / num_of_servers) + 1
    # check if specified directory exists. If not then create one
    if not os.path.exists(todir):  
        os.mkdir(todir) 
    else:
        pass
    partnum = 0
    # open file in read binary mode on windows
    input = open(fromfile, 'rb') 
    while 1:  
        chunk = input.read(chunksize)
        if not chunk: break
        partnum = partnum + 1
        # Join path components
        filename = os.path.join(todir, ('part%04d' % partnum)) 
        fileobj = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()  
    input.close()
    # throw an exception if specified condition does not meet
    assert partnum <= 9999  
    return partnum

# This function sends the file via clientsocket
def file_sender(file_name,clientsocket):
    path = "file_out/"+file_name
    file = open(path, 'rb')
    data = file.read(1024)
    while (data):
        clientsocket.send(data)
        data = file.read(1024)


def file_lister(path):
    """ 
    This function lists all files of a directory using os.walk() 
    and add them to a list 
    """
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        f.extend(filenames)
    return f

# Function for sending messages to the client
def message_sender(message,clientsocket):
    data = message.encode("utf-8")
    clientsocket.send(data)

# Function for creating socket
def socket_creator():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # reusing the socket
