# dev Config
import os
import logging


class Config(object):
    ENV = os.getenv("ENV", 'local')
    LOGGER_LEVEL = logging.INFO
    MODE = os.getenv("MODE", 'server')
    DB_CREDENTIALS = {
            "host":"localhost",
            "port":5432,
            "user":"cars24",
            "database":"hrms"
    }