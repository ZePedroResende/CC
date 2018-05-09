import hashlib
import json

def create_packet(data):
    #auth = hashlib.md5(json.dumps(data,sort_keys=True).encode('utf-8')).hexdigest()
    auth = ""
    return {'auth': auth, 'data': data}


def check_packet(packet):
    info = packet['data']
 #   auth = hashlib.md5(json.dumps(info,sort_keys=True).encode('utf-8')).hexdigest()
 #   if auth == packet['auth']:
    #    return info
    return info
 #   else:
 #       None
