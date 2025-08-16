import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

while 1:
    conn, addr = s.accept()
    print("Connected to ", addr)

    first_arr = []
    n1 = int.from_bytes(conn.recv(4), "big")
    for _ in range(n1):
        x = int.from_bytes(conn.recv(4), "big")
        first_arr.append(x)
    print("Received first arr: ", first_arr)


    second_arr = []
    n2 = int.from_bytes(conn.recv(4), "big")
    for _ in range(n2):
        x = int.from_bytes(conn.recv(4), "big")
        second_arr.append(x)
    print("Received second arr: ", second_arr)


    wanted_arr = []

    #error compar char cu char, nu nr cu nr
    for i in first_arr:
        for j in second_arr:
            if i == j:
                wanted_arr.append(i)


    print("Obtained array: ", wanted_arr)
    conn.send(int.to_bytes(len(wanted_arr), 4, "big"))
    for i in wanted_arr:
        conn.send(int.to_bytes(i, 4, "big"))    
s.close()
