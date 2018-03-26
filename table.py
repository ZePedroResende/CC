import threading


class table:
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
                     bandwidth, auth=None):
        return {'ip': ip, 'porta': porta, 'ram': float(ram.decode()),
                'cpu': float(cpu.decode()), 'rtt': float(rtt),
                'bandwidth': float(bandwidth), 'auth': auth,
                'n_times': 0}

    def print(self):
        print("\n")
        lista = []
        for v in self.server_list.values():
            m = len(str(v))
            lista.append(v)
        padding = (m-5) // 2
        print("-"*padding + "TABLE" + "-" * padding)
        for each in lista:
            print(each)
        print("-"*m)
        print(self.best_server())

    def best_server(self):
        print("1")

        def media(d):
            d = d[1]
            media = (d['ram'] + d['cpu'] + d['bandwidth'])/3
            load = media <= 70
            time = d['rtt'] < 60
            return load and time

        with self.lock:
            print("2")
            lista = sorted(self.server_list.items(),
                           key=lambda x: x[1]['n_times'])
            print("3")
            filt = list(filter(lambda x: media(x), lista))
            print("4")
            if not filt:
                res = lista[0][1]
            else:
                res = filt[0][1]
            self.server_list[res['ip']]['n_times'] += 1
            print("5")
            return res
