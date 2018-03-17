import threading


class Box:
    def __init__(self):

    def update_server(self):

class Table:
    def __init__(self):
        server_list={}
        self.lock = threading.RLock()

    def add_server(self,server):
        with self.lock
            server_list[server[ip]] = server
    def remove_server(self,server):
        with self.lock


    def update_server(self,server):
        with self.lock
