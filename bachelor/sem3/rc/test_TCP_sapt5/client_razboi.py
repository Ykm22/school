import socket
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 2222

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((TCP_IP, TCP_PORT))

print("Give n between , 4 <= n <= 9")
n = str(input("n = "))
c.send(n)

start_msg = c.recv(1024)
print(start_msg)

mistakes = 0
planes_alive = n
n = int(n)
print("Lines and columns between 0 and ", n - 1)
while 1:
    guessing_line = str(input("Guess line: "))
    c.send(guessing_line)
    guessing_column = str(input("Guess column: "))
    c.send(guessing_column)

    hit = c.recv(1024)
    print(hit)
    mistakes = int(c.recv(1024))
    print("Mistakes: ", mistakes)
    if mistakes == 5:
        break
    planes_alive = int(c.recv(1024))
    print("Planes alive: ", planes_alive)
    if planes_alive == 0:
        break

result = c.recv(1024)

if result == "Loss":
    print("Game lost")
else:
    print("Game won")

c.close()
