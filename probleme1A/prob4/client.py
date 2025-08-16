import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 7775

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))

Message = str(raw_input('Primul sir ordonat:'))
c.send(Message)
print 'Sent to server', Message

Message = str(raw_input('Al 2-lea sir ordonat:'))
c.send(Message)
print 'Sent to server', Message

data = c.recv(1000)
print 'Recieved from server', data

