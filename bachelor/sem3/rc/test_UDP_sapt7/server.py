import os
import socket
from collections import defaultdict
import operator
import sys

def prim(x):
    d = 0
    for i in range(1, x + 1):
        if x % i == 0:
            d += 1
    if d == 2:
        return True
    return False

def lista_divizori(x):
    list = []
    for i in range(2, x):
        if x % i == 0:
            list.append(x)
    return list

def run():
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_fd.bind((IP, PORT))
    while 1:
        n, addr = server_fd.recvfrom(4)
        ip = addr[0]
        print(f'Connection from {addr}')
        
        n = int.from_bytes(n, "big")
        v = []
        list_divizori_all = []
        for _ in range(n):
            x = int.from_bytes(server_fd.recvfrom(4)[0], "big")
            v.append(x)
            if prim(x) == False:
                list = lista_divizori(x)
                list_divizori_all += list
            print(v)
            #print(list_divizori_all)
        frecv = {}
        for x in list_divizori_all:
            if x in frecv:
                frecv[x] += 1
            else:
                frecv[x] = 1
        sorted_frecv = sorted(frecv.items(), key=operator.itemgetter(1), reverse=True)
        print("Top frecv: ", sorted_frecv[0][1], sorted_frecv[1][1], sorted_frecv[2][1])
        
        new_port = int(input('Give port between 45000 and 55000: '))


        new_addr = ip, new_port
        idk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        idk.bind(new_addr)
        idk.sendto(int.to_bytes(len("Start joc"), 4, "big"), addr)
        idk.sendto("Start joc".encode(), addr)

        first = False
        second = False
        third = False
        mistakes = 0
        while mistakes < 5:
            guess = int.from_bytes(server_fd.recvfrom(4)[0], "big")
            if guess == sorted_frecv[0][1]:
                if first == False:
                    first = True
                    server_fd.sendto(int.to_bytes(6, 4, "big"), new_addr)
                    server_fd.sendto("Corect".encode(), new_addr)
                elif first == True:
                    server_fd.sendto(int.to_bytes(8, 4, "big"), new_addr)
                    server_fd.sendto("Incorect".encode(), new_addr)
                    mistakes += 1
            if guess == sorted_frecv[1][1]:
                if second == False:
                    second = True
                    server_fd.sendto(int.to_bytes(6, 4, "big"), new_addr)
                    server_fd.sendto("Corect".encode(), new_addr)
                elif second == True:
                    server_fd.sendto(int.to_bytes(8, 4, "big"), new_addr)
                    server_fd.sendto("Incorect".encode(), new_addr)
                    mistakes += 1
            if guess == sorted_frecv[2][1]:
                if third == False:
                    third = True
                    server_fd.sendto(int.to_bytes(6, 4, "big"), new_addr)
                    server_fd.sendto("Corect".encode(), new_addr)
                elif third == True:
                    server_fd.sendto(int.to_bytes(8, 4, "big"), new_addr)
                    server_fd.sendto("Incorect".encode(), new_addr)
                    mistakes += 1
            

if __name__ == '__main__':
    run()