import threading


class Table:
    def __init__(self):
        self.server_list = {}
        self.lock = threading.RLock()

    def add_server(self, info):
        with self.lock:
            self.server_list[info['ip']] = info

    def remove_server(self, server):
        with self.lock:
            del self.server_list[server['ip']]

    def build_server(self, ip, porta, ram, cpu, rtt,
                     bandwidth=None, auth=None):
        return {'ip': ip, 'porta': porta, 'ram': ram,
                'cpu': cpu, 'rtt': rtt, 'bandwidth': bandwidth,
                'auth': auth}
