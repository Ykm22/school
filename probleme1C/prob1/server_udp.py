import os
import socket

def child(addr, IP, CHILD_PORT):
    server_child_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_child_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_child_fd.bind((IP, CHILD_PORT))
    server_child_fd.sendto(int.to_bytes(CHILD_PORT, 4, "big"), addr)

    a = int.from_bytes(server_child_fd.recvfrom(4)[0], "big")
    b = int.from_bytes(server_child_fd.recvfrom(4)[0], "big")
    sum = a + b
    server_child_fd.sendto(int.to_bytes(sum, 4, "big"), addr)
    os._exit(0)

def run():
    IP = "127.0.0.1"
    PORT = 2222
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_fd.bind((IP, PORT))
    while 1:
        addr = server_fd.recvfrom(0)[1]
        PORT += 1 
        if os.fork() == 0:
            child(addr, IP, PORT)

if __name__ == '__main__':
    run()