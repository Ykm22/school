from re import T
import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 3333

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

while 1:
    conn, addr = s.accept()
    print('Connected to', addr)

    string_len = int.from_bytes(conn.recv(4), "big")
    string = conn.recv(string_len).decode()
    print('Received string', string)

    substring_start = int.from_bytes(conn.recv(4), "big") - 1
    print('Start of substring ', substring_start + 1)

    wanted_length = int.from_bytes(conn.recv(4), "big")
    print('Wanted substring length', wanted_length)
	
    substring_wanted = ""

    if substring_start + wanted_length >= len(string):
        print('Too big substring wanted')
    else:
        for i in range(substring_start, substring_start + wanted_length):
            substring_wanted += string[i]
        print("Sent to client ", substring_wanted)
        conn.send(int.to_bytes(len(substring_wanted), 4, "big"))
        conn.send(substring_wanted.encode())
s.close()
