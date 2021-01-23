import socket
import sys
import time

HOST = '192.168.0.120'
PORT = 8001

u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("socket created")
try:
    u.bind((HOST, PORT))
except socket.error as e:
    print("Bind Failed, Error code: {}, Message: {}".format(err[0], err[1]))
    sys.exit()
print("socket bind success")
botaddr = [0, 0]
while True:
    data, addr = u.recvfrom(1024)
    print("connect from {}:{}".format(addr[0], addr[1]))
    print(data)
    if 'BOT' in data:
        botaddr[0] = addr[0]
        botaddr[1] = addr[1]
    else:
        u.sendto(data, (botaddr[0], botaddr[1]))


