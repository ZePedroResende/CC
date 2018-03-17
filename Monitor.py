#!/usr/bin/python3
import socket
import json
import time
import threading


class probe:
    def __init__(self):
        self.MCAST_GRP = '239.8.8.8'
        self.MCAST_PORT = 8888
        self.MSG = self.pack()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                    socket.IPPROTO_UDP)
        self.initSocket()
        self.start_updater()
        self._probe()

    def start_updater(self):
        def worker_updater(u):
            u.response()

        u = updater(self.socket)
        t = threading.Thread(target=worker_updater, args=(u,))
        t.daemon = True
        t.start()

    def pack(self):
        return json.dumps({"msg": "probe"}, separators=(',', ':')).encode()

    def initSocket(self):
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def _probe(self):
        while True:
            self.socket.sendto(self.MSG, (self.MCAST_GRP, self.MCAST_PORT))


class updater:
    def __init__(self, sock):
        self.MCAST_PORT = 8888
        self.s = sock

    def response(self):
        while True:
            msg = self.s.recv(1024).decode()
            print(msg)


if __name__ == '__main__':
    t1 = threading.Thread(target=probe())
    t1.start()
