#!/usr/bin/python3
import socket

MCAST_GRP = '239.8.8.8'
MCAST_PORT = 8888
MSG = "Hello World"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sock.sendto(MSG.encode(), (MCAST_GRP, MCAST_PORT))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.bind(('172.26.71.194', MCAST_PORT))
while True:
    msg = sock.recv(1024).decode()
    print(msg)
