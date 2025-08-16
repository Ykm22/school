import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 5555

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))

first_arr = str(raw_input("First array: "))
c.send(first_arr)

second_arr = str(raw_input("Second array: "))
c.send(second_arr)

wanted_arr = c.recv(1024)
print("Received ", wanted_arr)
