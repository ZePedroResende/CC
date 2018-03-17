#!/usr/bin/python3
import socket
import struct


class Agente:
    def __init__(self):
        self.MCAST_GRP = '239.8.8.8'
        self.MCAST_PORT = 8888
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                    socket.IPPROTO_UDP)
        self.init_socket()
        self.start_listening()

    def init_socket(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.MCAST_GRP, self.MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP),
                           socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                               mreq)

    def start_listening(self):
        def get_pack():
            return "OLA"
        while True:
            print("ASDS")
            request, to = self.socket.recvfrom(10240)
            request = request.decode()
            print(request, to)
            self.socket.sendto((get_pack()).encode(), to)


if __name__ == '__main__':
    Agente()
