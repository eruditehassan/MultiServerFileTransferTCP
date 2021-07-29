import os
from socket import *


def join(fromdir, tofile):
    """ 
This function joins all files present in the specified directory 
that were created by the split function in the server file. 
"""
    output = open(tofile, 'wb')  # opens file in write binary mode
    parts  = os.listdir(fromdir) # list all files in the specified directory
    parts.sort(  )               # sorts the files  
    for filename in parts:
        filepath = os.path.join(fromdir, filename) # Join path components 
        fileobj  = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(1024) 
            if not filebytes: break
            output.write(filebytes)
        fileobj.close(  )
    output.close(  )
    

        

