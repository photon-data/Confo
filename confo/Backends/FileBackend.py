# **************************************************************************#
# Title:                    FileBackend                                     #
# Description:              This backend is used to handle local            #
#                           file configurations                             #
# Author:                   Kabelo Masemola <kabelo.masemola@maskab.co.za>  #
# Original Date:            06 March 2021                                   #
# Update Date:              14 March 2021                                   #
# Version:                  0.1.0                                           #
# **************************************************************************#

# Import modules

from .AbstractBackend import AbstractBackend
import os
import json
from json.decoder import JSONDecodeError

from ..Exceptions import *

class FileBackend(AbstractBackend):

    def __init__(self):
        self.configuration_files = []
        self.configurations = {}
        self.namespace_name = '*'
        self.namespaces = []
        self.credentials = None
        self.config_path = None

    def load_credentials(self, credentials):
        def get_conf_name(file):
            if "." in file:
                return file.split('.')[0]
            else:
                return file

        def get_conf_values(namespace, file):
            data = None
            try:
                with open(self.config_path + "/" + namespace + "/" + file, "r") as f:
                    data = json.loads(f.read())
            except FileNotFoundError:
                print("Configuration file: " + file + " does not exist in namespace: " + namespace)
            except JSONDecodeError:
                print("Configuration file: " + file + " in namespace: " + namespace + " has unknown format")

            return data

        self.credentials = credentials
        self.config_path = credentials["config_path"]
        self.namespaces = os.listdir(self.config_path)
        for namespace in self.namespaces:
            if namespace not in list(self.configurations.keys()):
                self.configurations[namespace] = {}
            for conf_file in os.listdir(self.config_path + "/" + namespace):
                self.configurations[namespace][get_conf_name(conf_file)] = get_conf_values(namespace, conf_file)

    def create_namespace(self, namespace):
        try:
            os.mkdir(self.config_path + "/" + namespace)
        except FileExistsError:
            print("namespace " + namespace + " already exists")

        self.namespaces = os.listdir(self.config_path)

    def reload(self):
        # self.configurations = {}
        self.configuration_files = []
        self.load_credentials(credentials=self.credentials)

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

    def persist_everything(self):
        for namespace in self.namespaces:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace):
        if os.path.exists(self.config_path + "/" + namespace):
            pass
        else:
            os.mkdir(self.config_path + "/" + namespace)
        for configuration in self.configurations[namespace]:
            self.persist_configuration(namespace, configuration)

    def persist_configuration(self, namespace, configuration):
        with open(self.config_path + "/" + namespace + "/" + configuration + ".json", "w+") as f:
            data = self.configurations[namespace][configuration]
            f.write(json.dumps(data))
