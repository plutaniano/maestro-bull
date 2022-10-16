import os
from bull.core.settings.base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
CORS_ALLOW_ALL_ORIGINS = True
