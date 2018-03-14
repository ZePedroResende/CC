#!/usr/bin/python3
import socket


class probe:
    def __init__(self):
        self.MCAST_GRP = '239.8.8.8'
        self.MCAST_PORT = 8888
        MSG = "Hello World"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                    socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.socket.sendto(MSG.encode(), (self.MCAST_GRP, self.MCAST_PORT))


class updater:
    def __init__(self):
        self.MCAST_PORT = 8888
        self.s = socket.socket(socket.AF_INET,
                               socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.bind(('172.26.71.194', self.MCAST_PORT))
        while True:
            msg = self.s.recv(1024).decode()
            print(msg)
