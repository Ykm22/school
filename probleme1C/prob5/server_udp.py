import os
import socket

def div_sum(n):
    sum = 0
    for i in range(1, n + 1):
        if n % i == 0:
            sum += i
    return sum

def child(addr, IP, CHILD_PORT):
    #creating new socket for each connection
    server_child_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_child_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_child_fd.bind((IP, CHILD_PORT))
    #sending new port to the specific client to start sending datagrams to this fd
    server_child_fd.sendto(int.to_bytes(CHILD_PORT, 4, "big"), addr)

    #start

    n = int.from_bytes(server_child_fd.recvfrom(2)[0], "big")
    sum = div_sum(n)

    server_child_fd.sendto(int.to_bytes(sum, 4, "big"), addr)

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
        print(f'Connection from {addr}')
        PORT += 1 
        if os.fork() == 0:
            child(addr, IP, PORT)

if __name__ == '__main__':
    run()