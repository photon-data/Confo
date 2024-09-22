# ************************************************************************#
# Title:                    Confo                                         #
# Description:              This is the package main interface            #
# Author:                   Kabelo Masemola <kabelo.masemola@maskab.co.za>#
# Original Date:            15 March 2021                                 #
# Update Date:              15 March 2021                                 #
# Version:                  0.1.0                                         #
# ************************************************************************#

# Import modules

from .Backends import *
from singleton_decorator import singleton
from .Backends import *
from .Exceptions import *


# Make sure a backend is activated before any of its operations are used
def validate_backend(func):
    def wrapper(self, *arg, **kw):
        backends = self.get_backends()["all_backends"]
        if (self.active_backend_name != None) and (self.active_backend_name in backends):
            pass
        else:
            raise BackendsActivationException("Please activate a backend before this operation")
        return func(self, *arg, **kw)

    return wrapper


@singleton
class Confo:
    backends = {}
    active_backend = None
    active_backend_name = None

    def load_backend(self, credentials, name, backend_type):
        backend_class = backend_selector(backend_type)
        backend = backend_class()
        backend.load_credentials(credentials=credentials)
        self.backends[name] = backend
        del backend

    def get_backends(self):
        return {"all_backends": list(self.backends.keys()), "active_backend": self.active_backend_name}


    def activate_backend(self, backend_name):
        if backend_name in self.get_backends()["all_backends"]:
            if self.active_backend != None:
                self.backends.pop(self.active_backend_name,None)
                self.backends[self.active_backend_name] = self.active_backend
            self.active_backend = None
            self.active_backend_name = None
            self.active_backend = self.backends[backend_name]
            self.active_backend_name = backend_name
        else:
            raise BackendNotFoundException(backend_name + " doesn't exist")

    @validate_backend
    def use_namespace(self, system_name):
        self.active_backend.use_namespace(system_name=system_name)

    @validate_backend
    def get_namespaces(self):
        return self.active_backend.get_namespaces()

    @validate_backend
    def create_namespace(self, namespace):
        self.active_backend.create_namespace(namespace)

    @validate_backend
    def get_all(self):
        return self.active_backend.get_all()

    @validate_backend
    def get(self, name, field=None):
        return self.active_backend.get(name, field)

    @validate_backend
    def set(self, config, field, value):
        self.active_backend.set(config, field, value)

    @validate_backend
    def persist(self, namespace=False, config=False):
        self.active_backend.persist(namespace, config)

    @validate_backend
    def get_count(self):
        return self.active_backend.get_count()

    @validate_backend
    def reload(self):
        self.active_backend.reload()
