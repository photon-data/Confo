
# Exceptions

class BackendsActivationException(Exception):
    pass

class BackendNotFoundException(Exception):
    pass

class FileNotFoundException(Exception):
    pass

class ZookeeperHostNotFoundException(Exception):
    pass

class ZookeeperPortNotFoundException(Exception):
    pass

class NamespaceExistsException(Exception):
    pass

class NamespaceNotLoadedException(Exception):
    pass