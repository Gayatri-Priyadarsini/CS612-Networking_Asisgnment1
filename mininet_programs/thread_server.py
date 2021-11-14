import time
import socket
from threading import Thread
#from SocketServer import ThreadingMixIn

#hostname = socket.gethostname()
#TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_IP='10.0.0.1'
#TCP_IP='localhost'
print(TCP_IP)
TCP_PORT = 12345
BUFFER_SIZE = 1024

print("-------Server listening for client requests-------")

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print(" New thread started for "+ip+":"+str(port))

    def run(self):
        start=time.time()
        conn.send(str.encode(str(ThreadCount)))
        #conn.send(str.encode("Please enter a filename"))
        #filename=conn.recv(1024)
        
        filename="1GBFile.txt"
        
        print("File requested by client: ",filename)
        f=open(filename,'rb')
        filesize=0
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                filesize = filesize+1
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break
        end=time.time()
        exec_time=end-start
        print("Download time: ",exec_time)
        filesize=filesize*BUFFER_SIZE
        th=round(((filesize*0.001)/exec_time),3)
        print("Throughput: ",th," K/sec")
        

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []


ThreadCount=0

def now(): # current time on server
    return time.ctime(time.time())

while True:
    tcpsock.listen(5)
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    print('at',now())
    newthread = ClientThread(ip,port,conn)
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

