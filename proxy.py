#!/usr/bin/python3
from table import table
from Monitor import probe
import socket
from queue import Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


class proxy:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_number = 0
        self.available = 0
        self.initSocket()
        self.table = table()
        self.queue = Queue(maxsize=0)
        self.pool = self.start_pool()
        self.start_monitor()
        self.listen()

    def initSocket(self):
        self.sock.bind(('', 80))
        self.sock.listen(1)

    def listen(self):
        while True:
            connection, client_address = self.sock.accept()
            self.queue.put(connection)

    def start_pool(self):

        def _proxyHandler():
            proxyHandler(self.queue, self.table)

        executor = ThreadPoolExecutor(max_workers=100)
        return executor.submit(_proxyHandler)

    def start_monitor(self):

        def _monitor(table):
            table.remote_start()

        u = probe(self.table, start=False)
        t = Thread(target=_monitor, args=(u,))
        t.daemon = False
        t.start()


class proxyHandler:
    def __init__(self, queue, table):
        self.queue = queue
        self.table = table
        self.comunicate()

    def comunicate(self):
        def loop(r, s):
            while True:
                data = r.recv(4096)
                if not data:
                    s.close()
                    break
                s.sendall(data)

        while True:
            com = self.queue.get()
            server_json = self.table.best_server()
            server = server_json['ip']
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server, 80))
            t1 = Thread(target=loop, args=(s, com,))
            t2 = Thread(target=loop, args=(com, s,))
            t1.daemon = False
            t2.daemon = False
            t1.start()
            t2.start()
            t1.join()
            t2.join()


if __name__ == '__main__':
    proxy()
