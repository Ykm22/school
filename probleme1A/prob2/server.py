import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
#s.listen(1)

while 1:
    #conn, addr = s.accept()
    #print('Connection address', addr)

    string_len, addr_client = s.recvfrom(4)
    string_len = int.from_bytes(string_len, "big")

    print('Length of string:', string_len)

    string, _ = s.recvfrom(string_len)
    string = string.decode()
    print("String:", string)
    cnt = 0
    for ch in string:
        if ch == ' ':
            cnt += 1
    print('Sent to client', cnt)
    s.sendto(int.to_bytes(cnt, 4, "big"), addr_client)

s.close()
