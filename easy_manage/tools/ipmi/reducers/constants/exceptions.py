class CorruptedBufferError(Exception):
    pass


class InvalidPathError(Exception):
    def __init__(self, path):
        self.path = '/'.join(path)
