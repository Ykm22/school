import socket
from ctypes import *

TCP_IP = "127.0.0.1"
TCP_PORT = 8884
#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((TCP_IP, TCP_PORT))
#server_socket.listen(5)

while 1:
    #conn, _ = server_socket.accept()
    n , _ = server_socket.recvfrom(4)
    n = int.from_bytes(n, "big")
    print("n = ", n)
    v = []
    for i in range(n):
        x , _ = server_socket.recvfrom(4)
        x = int.from_bytes(x, "big")
        v.append(x)
    sum = 0
    for c in v:
        sum += c

    print('Am trimis la client', sum)
    server_socket.sendto(int.to_bytes(sum, 4, "big"), (TCP_IP, TCP_PORT))

server_socket.close()
