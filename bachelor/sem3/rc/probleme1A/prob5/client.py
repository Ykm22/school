import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 6666

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))

Message = input("Give a number:")
c.send(str(Message))

data = c.recv(100)
print 'Received from sv', data
