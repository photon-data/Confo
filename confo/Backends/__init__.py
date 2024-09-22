FILE_BACKEND = 1
ZOOKEEPER_BACKEND = 2

from .FileBackend import FileBackend
from .ZookeeperBackend import ZookeeperBackend


def backend_selector(backend_type):
    if backend_type == FILE_BACKEND:
        return FileBackend
    elif backend_type == ZOOKEEPER_BACKEND:
        return ZookeeperBackend

