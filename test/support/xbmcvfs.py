import os


class File:
    def __init__(self, path, mode='r'):
        self.path = path
        self.mode = mode

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return ''

    def write(self, data):
        return len(data) if data else 0

    def close(self):
        return None


def exists(path):
    return os.path.exists(path)


def listdir(path):
    return [], []


def mkdir(path):
    return None


def rmdir(path, force=False):
    return None


def delete(path):
    return None


def rename(src, dst):
    return None


def translatePath(path):
    return path
