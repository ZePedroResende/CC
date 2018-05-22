#!/usr/bin/python3
import socket
import json
import time
import threading
from table import table
import atexit
from auth import check_packet, create_packet, encrypt, decrypt


class probe:
    def __init__(self, table, start=True):
        self.table = table
        self.MCAST_GRP = '239.8.8.8'
        self.MCAST_PORT = 8888
        self.MSG = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                    socket.IPPROTO_UDP)
        self.n_packet = 0
        self.initSocket()
        if start:
            self.remote_start()

    def start_updater(self):
        def worker_updater(u):
            u.response()

        u = updater(self.socket, self.table)
        t = threading.Thread(target=worker_updater, args=(u,))
        t.daemon = True
        t.start()

    def pack(self):
        self.n_packet += 1
        return encrypt(json.dumps(create_packet({'n_packet': self.n_packet,
                        'rtt': str(int(time.time()))}),
                                  separators=(',', ':')).encode())

    def initSocket(self):
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def _probe(self):
        while True:
            self.socket.sendto(self.pack(), (self.MCAST_GRP, self.MCAST_PORT))
            time.sleep(1)

    def remote_start(self):
        self.start_updater()
        self._probe()


class updater:
    def __init__(self, sock, table):
        self.MCAST_PORT = 8888
        self.s = sock
        self.table = table

    def response(self):
        while True:
            p, ip = self.s.recvfrom(1024)
            p = eval(p.decode())
            msg = check_packet(decrypt(p))
            if msg:
                msg['rtt'] = (float(time.time()) - float(msg['rtt']))
                msg['ip'] = ip[0]
                server_info = self.table.build_server(**msg)
                print(server_info)
                self.table.add_server(server_info)


def printable(t):
    t.print()


if __name__ == '__main__':
    t = table()
    atexit.register(printable, t)
    probe(t)
