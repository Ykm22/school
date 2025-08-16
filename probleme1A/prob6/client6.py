import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 3333

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))

msg = str(input("String for server: "))
c.send(msg)

ch = str(input("Character: "))
c.send(ch)

count = str(c.recv(1024))
print("Found", count, " times")
