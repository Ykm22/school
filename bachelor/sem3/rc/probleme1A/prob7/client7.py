import socket
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 3333

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))

msg = str(input("String for server: "))
c.send(msg)

start_substring = str(input("Start of wanted substring: "))
c.send(start_substring)

#time.sleep(0.01)

c.send("3")
#substring_length = str(input("Wanted substring length: "))
#c.send(substring_length)

substring_wanted = c.recv(1024)
print("Received from server: ", substring_wanted)

c.close()
