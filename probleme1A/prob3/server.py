import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 7776

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
#s.listen(1)

while 1:
    #conn, addr = s.accept()
    #print('Connection address', addr)

    string_len, addr = s.recvfrom(4)
    string_len = int.from_bytes(string_len, "big")

    string, _ = s.recvfrom(string_len)
    string = string.decode()
    reversed_string = string[::-1]

    print('Sent to client', reversed_string)
    s.sendto(reversed_string.encode(), addr)


s.close()
