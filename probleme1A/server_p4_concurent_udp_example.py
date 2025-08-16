import socket
import os

TCP_IP = "127.0.0.1"
TCP_PORT = 7775

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((TCP_IP, TCP_PORT))
#s.listen(1)

def child(addr, TCP_CHILD_PORT):
    s_child = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_child.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_child.bind((TCP_IP , TCP_CHILD_PORT))

    s_child.sendto(int.to_bytes(TCP_CHILD_PORT, 4, "big"), addr)

    string1_len, _ = s_child.recvfrom(4)
    string1_len = int.from_bytes(string1_len, "big")
    string1, _ = s_child.recvfrom(string1_len)
    string1 = string1.decode()
    print ('Received from client', string1)

    string2_len, _ = s_child.recvfrom(4)
    string2_len = int.from_bytes(string2_len, "big")
    string2, _ = s_child.recvfrom(string2_len)
    string2 = string2.decode()
    print ('Received from client', string2)

    Str = string1 + string2
    sorted_chars = sorted(Str)
    result = "".join(sorted_chars)

    print('Sent to client', result)
    result_string_len = len(result)
    s_child.sendto(int.to_bytes(result_string_len, 4, "big"), addr)
    s_child.sendto(result.encode(), addr)
    os._exit(0)

while 1:
    #conn, addr = s.accept()
    #print('Connection from', addr)

    _, addr = s.recvfrom(0)
    print('Connection from', addr)
    TCP_PORT += 1
    if os.fork() == 0:
        child(addr, TCP_PORT)

s.close()