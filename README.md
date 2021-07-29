# MultiServerFileTransferTCP

## Functionality
The Multi Server File Transfer program has the following functionalities:
1) Downloading a file from a single server
2) Downloading a file from multiple servers
    1. Creating any number of servers from within the program
    2. File segmentation on server side
    3. Multiple client instances to communicate with multiple servers
    4. File recombination on client end
3) Handling single server failure
4) Handling server failure in the case when all servers crash or do not respond (entire server failure handling)
5) Load Balancing
6) Download resuming
7) Flexibility of input given by users
    1. Specification of the number of servers, specific ports, interval between status reporting and address of the file location on server side
    2. Specification of the time interval between metric reporting, path of output directory, IP address of the server, list of port numbers and option to toggle resumeability
8) Output and download metric reporting
    1. Server status reporting and giving user ability to close any server
    2. Download progress reporting on client side including downloaded bytes and speed for each server and also summed for all the servers.
    
## Methodology for implementation
The methodology for implementation of all the major functionality and the reason for the choice of specific methodology wherever applicable.
### Basic Client / Server Implementation
Object Oriented implementation was used for both the client and server implementation, the reason to prefer OOP over procedural approach was because the Thread module from threading library was used and a sub class of it was used to create client and server objects, also it gives much more control and flexibility whenever new functionality had to be added and if anything had to be modified. Moreover, an object-oriented approach makes it much more intuitive to work with multiple server and client instances by treating them as objects.
### Using Multiple Servers
To use multiple servers multi-threading was utilized. It was accomplished using python’s threading library (specifically Thread module). The reason for choosing this specific library was because of its
extensive documentation and a lot of guideline available on the internet that made it easier to debug the program in case of problems.
File Segmentation and Recombination
To segment the file to be sent by server a small script was written, this script creates a chunk size according to the number of servers. Let’s say if the size of file is 100 MB and there are 4 servers, then the chunk size will be 25 MB (dividing 100 by 4). In that way each server is assigned exactly one file initially that it must send to the client. All servers have access to all the files in case of recovery from a server failure. A similar script was written for file recombination that first sorts the chunks just to make sure they are in the right order and then reads all the chunks and then combines them into a single file
### Handling Single Server Failure
In case when one of the servers crashes, client sends request to another available server and starts to the receive the file from the same byte position where the previous server left it. The methodology of detecting server failure is when the client does not receive any data and the received data is still less than the total file size.
Handling Entire Server Failure
When the entire server fails then it was handled using a very simple solution. A lot of solutions were tried, but the optimized and best solution was to use try and except blocks. The logic behind it was that whenever client tries to connect to a server, if there is a server failure it throws an exception and it closes the client program. The try except block was used such that whenever there was such an exception the client program would keep on trying to connect to the server by using recursion. Even if we try to connect to a server that does was never run, it will still keep waiting for the server to turn and whenever it does the client automatically starts receiving the files from it.
### Download Resuming
Download resuming was established by keeping track of the number of bytes received by the each client instance. Whenever client experiences a server failure, it connects one of the other available servers and sends it the chunk number that it wants to receive and also the exact byte position where the previous server left it (initially it is 0 so when first connection is established it doesn’t create an problem).
### Input /Output and Metric Reporting
Python’s argsparse library was utilized for this purpose which makes things very simple.
For showing status on server side and showing metric reporting on client side in parallel with the running instances of servers and clients, a separate class was created that accesses the required attributes from server or client objects and reports them in the manner necessary. This approach was used because the attributes of running threads would not have been accessible by main thread in parallel, it would only have accessed them when the threads had finished executing.
One thing worth mentioning on server side status reporting is to allow user to close any server. For this purpose, threading library’s Timer module was utilized that combined with recursion allows user to enter input using keyboard before the next status report is displayed.
