#!/usr/bin/python3
import socket
import json
import time
import threading
import atexit
from table import table


class probe:
    def __init__(self, table):
        self.MCAST_GRP = '239.8.8.8'
        self.MCAST_PORT = 8888
        self.MSG = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                    socket.IPPROTO_UDP)
        self.initSocket()
        self.start_updater(table)
        self._probe()

    def start_updater(self, table):
        def worker_updater(u):
            u.response()

        u = updater(self.socket, table)
        t = threading.Thread(target=worker_updater, args=(u,))
        t.daemon = True
        t.start()

    def pack(self):
        return json.dumps({'rtt': str(int(time.time())), 'auth': ""},
                          separators=(',', ':')).encode()

    def initSocket(self):
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def _probe(self):
        while True:
            self.socket.sendto(self.pack(), (self.MCAST_GRP, self.MCAST_PORT))
            time.sleep(1)


class updater:
    def __init__(self, sock, table):
        self.MCAST_PORT = 8888
        self.s = sock
        self.table = table

    def response(self):
        while True:
            msg = eval(self.s.recv(1024).decode())
            server_info = self.table.build_server(**msg)
            print(server_info)
            self.table.add_server(server_info)


def printable(table):
    print(table)


if __name__ == '__main__':
    t = table()
    atexit.register(printable, t)
    probe(t)
