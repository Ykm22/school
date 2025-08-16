import socket
import os

TCP_IP = "127.0.0.1"
TCP_PORT = 3333

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)
    
def child(conn):
    string_len = int.from_bytes(conn.recv(4), "big")
    print('string_len =', string_len)
    string = conn.recv(string_len).decode()
    print('Received ', string)

    char = conn.recv(1).decode()
    print('Char: ', char)

    count = 0
    pos_string = ""
    for i in range(string_len):
        if string[i] == char:
            count = count + 1
            pos_string += str(i) + " " 
    print("Sent ", count)
    conn.send(int.to_bytes(count, 4, "big"))
    string_len = len(string)

    conn.send(int.to_bytes(string_len, 4, "big"))
    conn.send(pos_string.encode())

    conn.close()
    os._exit(0)

while 1:
    conn, addr = s.accept()
    print("Connection from", addr)
    if os.fork() == 0:
        child(conn)
