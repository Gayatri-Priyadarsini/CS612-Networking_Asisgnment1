import socket                   # Import socket module

s = socket.socket()             # Create a socket object
#host = socket.gethostname()     # Get local machine name
#hostname = socket. gethostname()
#print(hostname)
#host = socket.gethostbyname(hostname)
host='10.0.0.1'
#host='localhost'
print(host)
port = 12345                    # Reserve a port for your service.

s.connect((host, port))
client_no=s.recv(10)
print("Client number:",client_no)
#data=s.recv(1024)
#print("Message from server-",data)
#s.send(str.encode(input("Enter the filename to downloaded:")))
 
with open(str(client_no)+'.txt', 'wb') as f:
#with open('client.txt','wb') as f:
    print('file opened')
    print('receiving data...')
    while True:
        data = s.recv(1024)
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
