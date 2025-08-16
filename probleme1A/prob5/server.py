import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    
    n = int.from_bytes(conn.recv(4), "big")

    dividers = ""
    for i in range(1, n + 1):
        if n % i == 0:
            dividers += str(i) + " "
    print('Sent to client', dividers)
    dividers_len = len(dividers)
    conn.send(int.to_bytes(dividers_len, 4, "big"))
    conn.send(dividers.encode())
