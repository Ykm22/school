#test
import socket
import random
import time
import os

TCP_IP = "127.0.0.1"
TCP_PORT = 2222

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)

def child(conn):
    n = int.from_bytes(conn.recv(4), "big")

    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        line = random.randint(0, n - 1)
        column = random.randint(0, n - 1)
        matrix[line][column] = 1
    conn.send(("Game started").encode())

    planes_alive = n
    mistakes = 0
    while 1:
        guessing_line = int.from_bytes(conn.recv(4), "big")
        guessing_column = int.from_bytes(conn.recv(4), "big")

        bombardat = False
        if matrix[guessing_line][guessing_column] == 1:
            bombardat = True
        if bombardat == False:
            conn.send(("NU").encode())
            mistakes += 1
        else:
            conn.send(("DA").encode())
            planes_alive -= 1
        if mistakes == 5:
            conn.send(int.to_bytes(mistakes, 4, "big"))
            conn.send(int.to_bytes(4, 4, "big"))
            conn.send(("Loss").encode())
            break
        elif planes_alive == 0:
            conn.send(int.to_bytes(mistakes, 4, "big"))
            conn.send(int.to_bytes(mistakes, 4, "big"))
            conn.send(int.to_bytes(3, 4, "big"))
            conn.send(("Win").encode())
            break
        conn.send(int.to_bytes(mistakes, 4, "big"))
        conn.send(int.to_bytes(planes_alive, 4, "big"))
    conn.close()
    os._exit(0)

while 1:
    conn, addr = s.accept()
    print('Connected to', addr)
    if os.fork() == 0:
        child(conn)

s.close()
