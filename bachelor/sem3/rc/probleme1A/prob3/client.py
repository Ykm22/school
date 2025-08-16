import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 7776

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))

MESSAGE = str(raw_input('Give a message: '))
c.send(MESSAGE)
data = c.recv(10)
c.close()
print 'Received from server', data
