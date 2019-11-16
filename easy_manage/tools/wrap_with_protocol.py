from easy_manage.protocols import Protocols

def proto_wrap(data, proto: Protocols):
    return {
        'payload': data,
        'protocol': proto,
    }
