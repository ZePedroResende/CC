#!/usr/bin/python3
import socket
import struct
import subprocess
import json
import time
from random import randint
from auth import check_packet, create_packet


class Agente:
    def __init__(self):
        self.MCAST_GRP = '239.8.8.8'
        self.MCAST_PORT = 8888
        self.n_packet = 0
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
            porta = self.MCAST_PORT
            ram = run_bash("head -2 /proc/meminfo | grep -Po '[0-9]+'"
                           + "|sed -e ':a' -e 'N' -e '$!ba' -e 's/\\n/ /g'"
                           + "|awk -F ' ' '{print ((($1 - $2) / $1) * 100)}'")

            bandwidth = int(run_bash("netstat | grep tcp | wc -l")
                            ) / int(run_bash("ulimit -n")) * 100
            cpu = run_bash(
             "uptime | awk -F'[a-z]:' '{ print $2}' | awk -F ',' '{print $1}'")
            return create_packet({'ip': "", 'porta': str(porta), 'ram': ram.decode('utf-8'),
                                  'cpu': cpu.decode('utf-8'), 'rtt': msg['rtt'],
                                  'bandwidth': bandwidth})
        while True:
            request, to = self.socket.recvfrom(10240)
            packet = json.loads(request.decode())
            request = check_packet(packet)
            if request:
                if request['n_packet'] > self.n_packet:
                    self.n_packet = request['n_packet']
                    print(request, to)
                    msg = (str(get_pack(request))).encode()
                    time.sleep(randint(0, 10))
                    self.socket.sendto(msg, to)


if __name__ == '__main__':
    Agente()
