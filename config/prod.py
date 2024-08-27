# dev Config
import os
import logging


class Config(object):
    ENV = os.getenv("ENV", 'local')
    LOGGER_LEVEL = logging.INFO
    MODE = os.getenv("MODE", 'server')
    DB_CREDENTIALS = {
        "host":os.getenv("host"),
        "port":os.getenv("port"),
        "user":os.getenv("user"),
        "database":os.getenv("database"),
        "password":os.getenv("password")
    }