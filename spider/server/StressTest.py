import socket
import threading
import time
import json

class RequestThread(threading.Thread):
    def __init__(self):
        host = 'localhost'
        port = 7070
        self.socket = socket.socket()
        self.socket.connect((host ,port))
        self.data =  json.dumps({'action': 'postdata', 'data': ['1234567890']*100})+ '\r\n'
        self.success_count = 0
        self.stoped = False
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not self.stoped:
                self.socket.send(self.data)
                data = self.socket.recv(1024)
                if data:
                    #print data
                    self.success_count += 1
                #s.close()
            else:
                break

count = 500
threads = [RequestThread() for i in range(count)]

start_time = time.time()
for t in threads:
    t.setDaemon(True)
    t.start()

word = ''
while True:
    word = raw_input("enter q to quit:")
    if word == "q":
        for t in threads:
            t.stoped = True
        break
    else:
        time_span = time.time() - start_time
        all_count = 0
        for t in threads:
            all_count += t.success_count
        print "%s Request/Second" % str(all_count / time_span)
