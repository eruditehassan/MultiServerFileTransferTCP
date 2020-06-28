from server_module import server_thread_creator
from threading import Thread
import time
num_of_servers = 4
id = 1

class Server(Thread):
   def __init__(self):
      global id
      Thread.__init__(self)
      self.threadID = id
      id += 1

   def run(self):
      server_thread_creator(num_of_servers, self.threadID)

   def stop(self):
       self._is_running = False


threads = []
for i in range(num_of_servers):
    t = Server()
    t.daemon = True
    t.start()
    threads.append(t)

time.sleep(1)
threads[1].stop()




