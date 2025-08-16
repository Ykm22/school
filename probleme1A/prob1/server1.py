import socket
from ctypes import *
import sys

TCP_IP = "127.0.0.1"
TCP_PORT = 8884
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print('Connection address:', addr)
    data = conn.recv(sys.getsizeof(int))

    n = int.from_bytes(data, byteorder='little')
    print("n = ",n)
    v = []
    #for i in range(1, n + 1):
    x = int.from_bytes(conn.recv(sys.getsizeof(int)), byteorder='little')
    print(x)
    
    print('Am primit de la client', v)
    if not data: break
    sum = 0
    for c in data.split():
        if c.isdigit():
            sum += int(c)

    print('Am trimis la client', sum)
    conn.send(str(sum))

conn.close()
