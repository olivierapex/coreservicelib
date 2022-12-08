#! /usr/bin/python3
# -*- coding: utf-8 -*-

""" Example application  Module using Core Class """

from core_service_lib.core import Core


class App:
    """ Example application  Module using Core Class """

    def __init__(self, config_file_path):
        """ Init function adding flask path. """
        self.app_core = Core(app_name=__name__, config_file_path=config_file_path)
        self.app_core.add_url_rule("/health", "health", self.health, methods=["GET"])

    def health(self):
        """Service health"""
        return {"STATUS": "OK", "INITIATED_CLASS": str(self)}

    def run(self):
        """ Run function that initiate the App Class and run the Flask framework. """
        self.app_core.logger.info("Starting service endpoint.")
        return self.app_core.run(host=self.app_core.conf.host_ip)


if __name__ == "__main__":
    api = App("/etc/app/config.json")
    wsgi_app = api.run()
