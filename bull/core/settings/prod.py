from bull.core.settings.base import *

DEBUG = False
STATIC_ROOT = os.path.join(BASE_DIR, "static")
ALLOWED_HOSTS = ["api.maestrocapital.com.br"]
CSRF_TRUSTED_ORIGINS = ["https://mais.maestroinvestimentos.com.br"]
CORS_ALLOWED_ORIGINS = [
    "https://mais.maestroinvestimentos.com.br",
    "https://hub.xpi.com.br",
]
CORS_ALLOW_CREDENTIALS = True
