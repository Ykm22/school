import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 7777
MESSAGE = str(raw_input('Dati un string: '))

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))
c.send(MESSAGE)
print 'Am trimis la server', MESSAGE
data = c.recv(10)
c.close()
print 'Am primit de la server', data
