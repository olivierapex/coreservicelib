#! /usr/bin/python3
# -*- coding: utf-8 -*-

""" Conf Module """

import logging
import os
import sys

import yaml

# import configparser


class Conf:
    """ Config Class that's reading config.yaml file and get value from it. """

    def __init__(self, config_file_path):
        if not os.path.isfile(config_file_path):
            logging.error("ERROR: Config file not found.")
        try:
            with open(config_file_path, "r") as yaml_data_file:
                self.conf = yaml.safe_load(yaml_data_file)
        except FileNotFoundError as err:
            logging.error(str(err))

    # Generique
    @property
    def config(self):
        """ Property return all the config file attributes. """
        return self.conf if self.config else None

    # Static Properties
    @property
    def log_info(self):
        """ Property return config logger information. """
        log = self.conf.get("log")
        if not log:
            logging.warning("Config param, log_info not defined.")
        return log

    @property
    def host_ip(self):
        """ Property return interface IP to run the service on. """
        host_ip = self.conf.get("host_ip")
        if not host_ip:
            logging.warning("Config param, host_ip not defined.")
        return host_ip

    def is_exist(self, nested_key):
        """ Tool function to check if a property exist in a nested Dict. Return the value or False. """
        result = False
        if self.conf:
            for key in self.config:  # This is only a 1 level nested dict.
                if nested_key in key:
                    result = key.get(nested_key)
        return result
