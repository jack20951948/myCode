import socket               
 
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname() 
port = 1025                
print('Host name:', host)
# s.bind((host, port))       # for windows
s.bind(('', port)) 
 
s.listen(5)                 
while True:
    c,addr = s.accept()     
    print('recive from address', addr)
    data = c.recv(1024)  
    print('recived data:',data.decode()) 
    # c.send('hello world')
    c.close()                
