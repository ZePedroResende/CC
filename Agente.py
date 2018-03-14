#!/usr/bin/python3
import socket
import struct
import sys

MCAST_GRP = '239.8.8.8'
MCAST_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    request, to = sock.recvfrom(10240)
    request = request.decode()
    print(request, to)
    sock.sendto((request + sys.argv[1]).encode(), to)
