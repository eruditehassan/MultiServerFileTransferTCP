from server_functions import *
from threading import Thread, Timer
import socket
import argparse
import time
import sys


# Argparse module helps in writing user-friendly 
# command-line interfaces. The argparse module 
# automatically generates help and usage messages 
# when an invalid argument is given. 
# Initializing the parser

parser = argparse.ArgumentParser()
#Add the  arguments
parser.add_argument("-i", metavar = "interval", type = int, default = 1, help = "Time interval in seconds between server status reporting")
parser.add_argument("-n", metavar = "num_servers", type = int, default = 4, help = "Total number of  virtual servers")
parser.add_argument("-f", metavar = "file_path", type = str, default = "file.mp4", help = "Address pointing to the file location")
parser.add_argument("-p", metavar = "ports", type = list, default =[65000,65001,65002,65003] , help = "List of port numbers(‘n’ port numbers, one for each server)")
# Execute the parse_args() method
args = parser.parse_args()

id = 1


#Define a class for threads
class NestedClientThread(Thread):
    
    # initialize the attributes of a class when object of the class is created
    def __init__(self, sock, port, f):
        Thread.__init__(self)
        self.port = port
        self.clientsocket = sock
        self.file_id = None
        self.byte_position = 0
        self.file_size = 0
        self.stop_thread = False
        self.f = f

    # Method for representing the thread's activity.
    def run(self):
        # check if a specified directory exists. If not, then create one
        if not(os.path.isdir("file_out")):
            os.mkdir("file_out")
        
        # recieve client_id form the client and store it in file_id
        self.file_id = int(self.clientsocket.recv(1024).decode('utf-8'))
        
        # path concatenation
        path = "file_out/" + self.f[self.file_id - 1]
        file = open(path, 'rb')
        
        # Retrieve size of the file that has to be sent to the client
        self.file_size = int(os.stat(path).st_size)
        self.clientsocket.send(str(self.file_size).encode("utf-8"))
        
        # recieve byte position from the client
        self.byte_position = int(self.clientsocket.recv(1024).decode('utf-8'))
        data = file.read(1024)
        while (data):
            self.clientsocket.send(data)
            data = file.read(1024)
            # check for the boolean value of stop_thread
            if self.stop_thread:
                break
        # close the socket
        self.clientsocket.close()



class Server(Thread):
    # used to initialize the attributes of a class when object of the class is created
    def __init__(self,port_no):
        global id
        global port
        Thread.__init__(self)
        self.threadID = id
        self.name = "Server " + str(self.threadID)
        
        # creating socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port_no
        self.file_size = 0
        self.clientsocket = 0
        self.client_addr = 0
        self.file_id = None
        self.byte_position = 0
        self.stop_thread = False
        self.threads = []
        id += 1


    def run(self):
        # splitting the specified file in n portions where n is args.n
        split(args.f, "file_out", args.n)
        # lists all splitted files in a directory named file_out
        f = file_lister("file_out")
        # Reusing the socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # binds the socket at specified host and port number
        self.sock.bind(("127.0.0.1", self.port))

        while True:
            # listen for all incomming connections
            self.sock.listen(5)
            # accept any incomming connection
            self.clientsocket, self.client_addr = self.sock.accept()
            
            # create new threads of NestedClientThread class type
            t = NestedClientThread(self.clientsocket, self.port, f)
            # prevent the threads from running in background
            t.daemon = True
            # start the threads
            t.start()
            
            # append the newly created threads into threads list
            self.threads.append(t)

        for t in self.threads:
            # causes the main thread of NestedClientThread class to wait until sub-threads finish execution
            t.join()


class metricReporting(Thread):
    def __init__(self, thread_list):
        Thread.__init__(self)
        self.threads = thread_list
        self.interval = args.i

    def run(self):
        answer = 0
        while True:
            # check for value entered by the user for shutting down the server
            if answer and (answer[0] == "E" or answer[0] == "e"):
                if (len(answer) == 2):
                    server_no = int(answer[-1])
                elif (len(answer) == 3):
                    server_no = int(answer[len(answer)-2:len(answer)])
                # shutdown the server with corresponding server nummber
                self.threads[server_no-1].stop_thread = True

            for i in range(len(self.threads)):
                t = self.threads[i]
                status = ""
                # check the status of the server
                if not(t.stop_thread):
                    status = "Alive"
                else:
                    status = "Dead"
                print("{}: Port: {} Status: {}, To Shutdown Server 1 Enter: E{}".format(t.name, t.port,status, t.threadID))
            print()
            timeout = 5
            t = Timer(timeout, self.run)
            t.start()
            # take input from the user
            answer = input()
            t.cancel()

# list for storing the threads
threads = []
for i in range(args.n):
    # create thread of Server class type
    t = Server(args.p[id - 1])
    print("Started server with port ", t.port)
    # prevent the threads from running in background
    t.daemon = True
    t.start()
    # append newly created threads in list holding all the threads
    threads.append(t)
    if (i == args.n - 1):
        # make list of only those threads whose type is Server class
        server_threads = [t for t in threads if type(t) == Server]
        # make thread of metricReporting class
        tm = metricReporting(server_threads)
        tm.daemon = True
        tm.start()
        threads.append(tm)

for t in threads[:args.n]:
    # causes main thread to wait until other threads finish executing
    t.join()





