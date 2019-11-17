from easy_manage.protocol import Protocol


def proto_wrap(data, proto: Protocol):
    return {
        'payload': data,
        'protocol': proto,
    }
