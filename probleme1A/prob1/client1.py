import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 8884
Message = str(raw_input("Dati un sir de numere: "))

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))
c.send(Message)
print 'Am trimis la server', Message
data = c.recv(10)
c.close()

print 'Am primit de la server:', data
