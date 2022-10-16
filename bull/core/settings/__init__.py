import os
from dotenv import load_dotenv

load_dotenv("./bull/core/settings/.base.env")

match os.environ.get("DJANGO_ENVIRONMENT"):
    case "PRODUCTION":
        load_dotenv("./bull/core/settings/.prod.env")
        from bull.core.settings.prod import *

    case "DEVELOPMENT":
        load_dotenv("./bull/core/settings/.dev.env")
        from bull.core.settings.dev import *

    case None:
        raise ValueError("DJANGO_ENVIRONMENT not set")

    case _:
        raise Exception("DJANGO_ENVIRONMENT is not a valid value")
