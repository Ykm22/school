import os
import socket

def child(addr, IP, CHILD_PORT):
    #creating new socket for each connection
    server_child_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_child_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_child_fd.bind((IP, CHILD_PORT))
    #sending new port to the specific client to start sending datagrams to this fd
    server_child_fd.sendto(b'0', addr)

    #start

    string_len = int.from_bytes(server_child_fd.recvfrom(4)[0], "big")
    string = server_child_fd.recvfrom(string_len + 4)[0].decode()
    print(string)
    ch = server_child_fd.recvfrom(1)[0].decode()

    print(f'String {string}, len {string_len}, ch {ch}')
    v = []
    for pos in range(string_len):
        if ch == string[pos]:
            v.append(pos + 1)
    print(v)
    v_len = len(v)
        
    server_child_fd.sendto(int.to_bytes(v_len, 4, "big"), addr)
    for pos in range(v_len):
        server_child_fd.sendto(int.to_bytes(v[pos], 4, "big"), addr)
    
    server_child_fd.close()

    os._exit(0)

def run():
    IP = "127.0.0.1"
    PORT = 2222
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_fd.bind((IP, PORT))
    while 1:
        addr = server_fd.recvfrom(0)[1]
        print(f'Connection from {addr[0]}')
        PORT += 1 
        if os.fork() == 0:
            child(addr, IP, PORT)

if __name__ == '__main__':
    run()