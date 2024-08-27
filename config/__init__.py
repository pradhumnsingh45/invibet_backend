import os

ENV = os.getenv("ENV", 'local')

if ENV == "prod":
    from .prod import Config

elif ENV == "dev":
    from .dev import Config

elif ENV == "local":
    from .local import Config

SETTINGS = Config