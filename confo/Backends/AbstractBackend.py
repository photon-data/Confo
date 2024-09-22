# **************************************************************************#
# Title:                    AbstractBackend                                 #
# Description:              This class defines a backend interface          #
# Author:                   Kabelo Masemola <kabelo.masemola@maskab.co.za>  #
# Original Date:            06 March 2021                                   #
# Update Date:              06 March 2021                                   #
# Version:                  0.1.0                                           #
# **************************************************************************#

# Import modules
from abc import ABC, abstractmethod
from ..Exceptions import *

class AbstractBackend(ABC):
    configurations = {}
    namespace_name = None
    namespaces = []

    @abstractmethod
    def load_credentials(self, credentials):
        pass

    def use_namespace(self, system_name):
        if system_name in self.get_namespaces()["all_namespaces"]:
            self.namespace_name = system_name
            self.reload()
        else:
            print("Namespace: " + system_name + " does not exist")

    def get_namespaces(self):
        namespaces = {"all_namespaces": self.namespaces, "current_namespace": self.namespace_name}
        return namespaces

    @abstractmethod
    def create_namespace(self, namespace):
        pass

    def get_all(self):
        if self.namespace_name in self.namespaces:
            return self.configurations[self.namespace_name]
        else:
            raise NamespaceNotLoadedException("Please select namespace")

    def get(self, name, field=None):
        if field != None:
            try:
                return self.configurations[self.namespace_name][name][field]
            except:
                print("configuration %s or field %s are not set" % (name, field))
        else:
            try:
                return self.configurations[self.namespace_name][name]
            except:
                print("configuration %s is not set" % (name))

    def set(self, config, field, value):
        if type(field) == str:
            try:
                self.configurations[self.namespace_name][config][field] = value
            except:
                self.configurations[self.namespace_name][config] = {}
                self.configurations[self.namespace_name][config][field] = value
        elif (type(field) == dict or type(field) == list) and value == None:
            try:
                self.configurations[self.namespace_name][config] = field

            except:
                pass

    @abstractmethod
    def persist(self, namespace, config):
        pass

    def get_count(self):
        return len(self.get_all())

    @abstractmethod
    def reload(self):
        pass
