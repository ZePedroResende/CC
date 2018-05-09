import hashlib
import bencode


def create_packet(data):
    auth = hashlib.md5(bencode.bencode(data)).hexdigest()
    return {'auth': auth, 'data': data}


def check_packet(packet):
    info = packet['data']
    auth = hashlib.md5(bencode.bencode(info)).hexdigest()
    if auth == packet['auth']:
        return info
    else:
        None
