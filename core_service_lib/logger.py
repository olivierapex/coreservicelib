#! /usr/bin/python3
# -*- coding: utf-8 -*-

""" Loggin Wrapper Module """

import logging

LOGLEVEL = {
    "DEBUG": logging.DEBUG,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "CRITICAL": logging.CRITICAL,
}
FORMATTER = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s")

loggers = {}


def setup_logger(name, path, level=logging.INFO):
    # pylint: disable=C0103, W0603, R1705
    """ Setup a Wrapper function of the class logging. """
    global loggers

    if loggers.get(name):
        return loggers.get(name)
    else:
        handler = logging.FileHandler(path)
        handler.setFormatter(FORMATTER)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        loggers[name] = logger
        return logger
