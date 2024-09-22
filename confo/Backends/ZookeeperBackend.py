# **************************************************************************#
# Title:                    ZookeeperBackend                                #
# Description:              This backend is used to handle distributed      #
#                            configuration                                  #
# Author:                   Kabelo Masemola <kabelo.masemola@maskab.co.za>  #
# Original Date:            14 March 2021                                   #
# Update Date:              14 March 2021                                   #
# Version:                  0.1.0                                           #
# **************************************************************************#

# Import modules

from .AbstractBackend import AbstractBackend
import os
import json
from json.decoder import JSONDecodeError
from kazoo.client import KazooClient
from ..Exceptions import *


class ZookeeperBackend(AbstractBackend):
    def __init__(self):
        self.configurations = {}
        self.zookeeper_host = None
        self.zookeeper_port = None
        self.zookeeper_user = None
        self.zookeeper_passwd = None
        self.zk_client = None
        self.namespace_name = '*'
        self.main_namespace = "/confo/"
        self.namespaces = None

    def load_credentials(self, credentials):
        self.parse_credentials(credentials)
        if (self.zookeeper_user == None) and (self.zookeeper_passwd == None):
            self.zk_client = KazooClient(hosts=self.zookeeper_host + ":" + str(self.zookeeper_port))
        else:
            auth_data = [("digest", self.zookeeper_user + ":" + self.zookeeper_passwd)]
            self.zk_client = KazooClient(hosts=self.zookeeper_host + ":" + self.zookeeper_port, auth_data=auth_data)
        self.zk_client.start()
        self.zk_client.ensure_path("/confo")
        self.namespaces = self.zk_client.get_children(self.main_namespace)

    def create_namespace(self, namespace):
        self.zk_client.ensure_path(self.main_namespace + namespace)
        self.namespaces = self.zk_client.get_children(self.main_namespace)

    def persist(self, namespace=False, config=False):
        if namespace == False:
            # Persist everything
            self.persist_everything()
        elif config == False:
            # persist the entire namespace if exists
            self.persist_namespace(namespace)
        else:
            # persist just one configuration file
            self.persist_configuration(namespace, config)

    def reload(self):
        self.configurations[self.namespace_name] = {}
        configs = self.zk_client.get_children(self.main_namespace + "/" + self.namespace_name)
        for config in configs:
            path = self.main_namespace + "/" + self.namespace_name + "/" + config
            data, stat = self.zk_client.get(path)
            if data.decode('utf-8').strip() == '':
                data = "{}"
            try:
                self.configurations[self.namespace_name][config] = json.loads(data)
            except ValueError as e:
                self.configurations[self.namespace_name][config] = json.loads("{}")

    def parse_credentials(self, credentials):
        if "zookeeper_user" in credentials.keys():
            self.zookeeper_user = credentials["zookeeper_user"]
        if "zookeeper_passwd" in credentials.keys():
            self.zookeeper_passwd = credentials["zookeeper_passwd"]
        if "zookeeper_host" in credentials.keys():
            self.zookeeper_host = credentials["zookeeper_host"]
        else:
            raise ZookeeperHostNotFoundException("Please set 'zookeeper_host' in credentials")
        if "zookeeper_port" in credentials.keys():
            self.zookeeper_port = credentials["zookeeper_port"]
        else:
            raise ZookeeperPortNotFoundException("Please set 'zookeeper_port' in credentials")

    def persist_everything(self):
        for namespace in self.namespaces:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace):
        recover_namespace = self.namespace_name
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace " + namespace + " not loaded. Load namespace with obj.use_namespace(" + namespace + ")")
        self.recover_config = self.configurations[namespace]
        if self.zk_client.exists(self.main_namespace + "/" + namespace):
            pass
        else:
            self.zk_client.ensure_path(self.main_namespace + "/" + namespace)

        self.use_namespace(namespace)
        for configuration in self.recover_config:
            self.persist_configuration(namespace, configuration)
        self.use_namespace(recover_namespace)

    def persist_configuration(self, namespace, configuration):
        self.recover_config = self.configurations[namespace]
        path = self.main_namespace + "/" + namespace + "/" + configuration
        self.zk_client.ensure_path(path)
        data = self.recover_config[configuration]
        self.zk_client.set(path, str.encode(json.dumps(data)))
