#!/usr/bin/python3
import socket
import struct
import subprocess
import time
import json


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
        def run_bash(cmd):
            return subprocess.check_output(['bash', '-c', cmd])

        def get_pack(msg):
            ip = self.socket.getsockname()[0]
            porta = self.MCAST_PORT
            ram = run_bash("head -2 /proc/meminfo | grep -Po '[0-9]+'")
            bandwidth = None
            cpu = run_bash(
             "uptime | awk -F'[a-z]:' '{ print $2}' | awk -F ',' '{print $1}'")

            rtt = str(int(time.time()) - int(msg['rtt']))
            auth = ""
            return {'ip': ip, 'porta': str(porta), 'ram': ram,
                               'cpu': cpu, 'rtt': rtt,
                               'bandwidth': bandwidth, 'auth': auth}
        while True:
            request, to = self.socket.recvfrom(10240)
            request = json.loads(request.decode())
            print(request, to)
            msg = (str(get_pack(request))).encode()
            self.socket.sendto(msg, to)


if __name__ == '__main__':
    Agente()
