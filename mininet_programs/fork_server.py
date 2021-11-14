import os, time, sys
import socket # get socket constructor and constants


TCP_IP = '10.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024

try:
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    threads = []
except socket.error as e:
    print(str(e))

def now(): # current time on server
    return time.ctime(time.time())

activeChildren = []
ProcessCount=0
def reapChildren(): # reap any dead child processes
    while activeChildren: # else may fill up system table
        pid,stat = os.waitpid(0, os.WNOHANG) # don't hang if no child exited
        if not pid: break
        activeChildren.remove(pid)

def handleClient(connection): # child process: reply, exit
    #time.sleep(5) # simulate a blocking activity
    #while 1: # read, write a client socket
    #    data = connection.recv(1024) # till eof when socket closed
    #    if not data: break
    #    connection.send('Echo=>%s at %s' % (data, now()))
    #    connection.close() 
    #    os._exit(0)
    
    connection.send(str.encode(str(ProcessCount)))
        #conn.send(str.encode("Please enter a filename"))
        #filename=conn.recv(1024)    
    start=time.time()
    filename="1GBFile.txt"
    
    print("File requested by client: ",filename)
    f=open(filename,'rb')
    filesize=0
    if (f):
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                filesize=filesize+1
                connection.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                end=time.time()
                exec_time=end-start
                print("Download time: ",exec_time)
                filesize=filesize*BUFFER_SIZE
                th=round(((filesize*0.001)/exec_time),3)
                print("Throughput: ",th," K/sec")
                connection.close()
                os._exit(0)
                break

while 1: # wait for next connection,
    tcpsock.listen(5)
    print("-------Server listening for client requests-------")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    print('at', now())
    ProcessCount += 1 
    reapChildren() # clean up exited children now
    childPid = os.fork() # copy this process
    if childPid == 0: # if in child process: handle       
        handleClient(conn)
    else: # else: go accept next connect
        activeChildren.append(childPid) # add to active child pid list


