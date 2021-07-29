from threading import Thread
import socket
import time
import argparse
import client_functions
import os


# Argparse module helps in writing user-friendly 
# command-line interfaces. The argparse module 
# automatically generates help and usage messages 
# when an invalid argument is given. 

# Initializing the parser
parser = argparse.ArgumentParser()
# Adding arguments
parser.add_argument("-i", metavar = "interval", type = int, default = 0.01, help = "Time interval in seconds between metric reporting")
parser.add_argument("-o", metavar = "output_path", type = str, default = "output", help = "path of output directory")
parser.add_argument("-a", metavar = "ip", type = str, default = "127.0.0.1", help = "IP address of server")
parser.add_argument("-p", metavar = "ports", type = list, default =[65000,65001,65002,65003] , help = "List of port numbers (one for each server)")
parser.add_argument("-r", metavar = "resume", type = bool, default = True, help = "Whether to resume the existing download in progress")
# Execute the parse_args() method
args = parser.parse_args()


server_host = args.a
client_id = 1

#Define a class for threads
class Client(Thread):
    # initialize the attributes of a class when object of the class is created
    def __init__(self):
        global client_id
        Thread.__init__(self)
        self.client_id = client_id
        # create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = args.p[self.client_id-1]
        self.total_bytes = 0
        self.file_size = 0
        self.speed_s = 0
        self.bytes_s = 0
        client_id += 1

    # Method for representing the thread's activity.
    def run(self):
        # check if a specified directory exists. If not, then create one
        if not(os.path.isdir("file_recv")):
            os.mkdir("file_recv")
        try:
            # connect to the server with hostname and port number
            self.sock.connect((server_host,self.server_port))
            print("Client {} connected to server with port {}".format(self.client_id, self.server_port))
            # send client_id to the server
            self.sock.send(str(self.client_id).encode('utf-8'))
            # recieve file size from the server
            self.file_size = int((self.sock.recv(1024)).decode('utf-8'))
            # send total bytes to the server
            self.sock.send(str(self.total_bytes).encode('utf-8'))
            filepath = "file_recv/part000{}".format(self.client_id)
            # open file in write binary mode in windows
            file = open(filepath, 'wb')
            data = self.sock.recv(1024)
            self.total_bytes += 1024
            while (data):
                file.write(data)
                data = self.sock.recv(1024)
                # check if client wants to resume the download
                if args.r:
                    if (len(data) == 0 and self.total_bytes < self.file_size):
                        if (self.client_id == 1):
                            self.server_port = args.p[self.client_id]
                        elif (self.client_id == len(args.p)):
                            self.server_port = args.p[self.client_id - 2]
                        else:
                            self.server_port = args.p[self.client_id]
                        self.run()
                self.total_bytes += 1024
            else:
                file.close()
            print("Client {} received its segment completely".format(self.client_id))
        except:
            # executes the run function incase of any exception
            self.run()


class metricReporting(Thread):
    def __init__(self, thread_list):
        Thread.__init__(self)
        self.threads = thread_list
        self.interval = args.i
        self.total_bytes = 0
        self.total_file_size = 0
        self.time_passed = 0
        self.download_speed = 0

    def run(self):
        for th in self.threads:
            # add size of the file recieved by every thread into total_file_size
            self.total_file_size += th.file_size
        while self.total_bytes < self.total_file_size:
            # sleep for interval specified by the client for metric reporting 
            time.sleep(self.interval)
            self.time_passed += self.interval
            for i in range(len(self.threads)):
                t = self.threads[i]
                # increment total bytes recieved by every thread into total bytes
                self.total_bytes += t.total_bytes
                # calculte download speed
                speed = (t.total_bytes / self.time_passed) / 1024
                self.download_speed += speed
                print("Server {}: {}/{}, download speed: {} kb/s".format(t.client_id, t.total_bytes,t.file_size,speed))
                # when all the threads in the list are iterated
                if i == len(self.threads) - 1:
                    print("Total: {}/{}, download speed: {} kb/s".format(self.total_bytes, self.total_file_size,self.download_speed))
            print()

# list for storing the threads
threads = []
num_of_servers = len(args.p)
for i in range(num_of_servers):
    # create a thread of Client class type
    t = Client()
    # prevent the threads from running in background
    t.daemon = True
    # start the thread
    t.start()
    # append newly created threads in list holding all the threads
    threads.append(t)
    # make list of only those threads whose type is Client class
    client_threads = [t for t in threads if type(t) == Client]
    if (i == num_of_servers - 1):
        # create thread of metricReporting class type
        tm = metricReporting(client_threads)
        tm.daemon = True
        tm.start()
        threads.append(tm)


for t in threads:
    # causes main thread to wait until other threads finish executing
    t.join()

# check if output directory specified by the user exists. If not, the create one    
if not(os.path.isdir(args.o)):
    os.mkdir(args.o)

# path concatenation
output_file_path = args.o + "/file_join.mp4"

# call to the join function which joins the files in specified directory
client_functions.join("file_recv", output_file_path)
