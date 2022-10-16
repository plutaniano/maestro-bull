import os
from pathlib import Path

AUTH_USER_MODEL = "user.User"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LANGUAGE_CODE = "pt-br"
ROOT_URLCONF = "bull.core.urls"
SECRET_KEY = os.environ["SECRET_KEY"]
STATIC_URL = "static/"
TIME_ZONE = "America/Sao_Paulo"
USE_TZ = True
USE_X_FORWARDED_HOST = True
WSGI_APPLICATION = "bull.core.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "bull.core.auth_backends.SlackBackend",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INSTALLED_APPS = [
    # Django Default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.postgres",
    "django.forms",
    # Apps
    "bull.apps.api",
    "bull.apps.reports",
    "bull.apps.slack",
    "bull.apps.user",
    "bull.apps.xpaccount",
    # Other
    "corsheaders",
    "django_celery_beat",
    "rest_framework",
    "django_filters",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(os.path.join(BASE_DIR, "templates"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DATABASE_NAME"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }
}

XP = {
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
}

CELERY = {
    "broker_url": "redis://localhost:6379",
    "RESULT_BACKEND": "redis://localhost:6379",
    "ACCEPT_CONTENT": ["application/json"],
    "TASK_SERIALIZER": "json",
    "RESULT_SERIALIZER": "json",
    "beat_scheduler": "django_celery_beat.schedulers:DatabaseScheduler",
}


HUBSPOT = {
    "API_KEY": os.environ["HUBSPOT_API_KEY"],
}

SLACK = {
    "BOT_ID": os.environ["SLACK_BOT_ID"],
    "BOT_USER_ID": os.environ["SLACK_BOT_USER_ID"],
    "CLIENT_ID": os.environ["SLACK_CLIENT_ID"],
    "CLIENT_SECRET": os.environ["SLACK_CLIENT_SECRET"],
    "SECRET_TOKEN": os.environ["SLACK_SECRET_TOKEN"],
    "SIGNING_SECRET": os.environ["SLACK_SIGNING_SECRET"],
    "TEAM_ID": os.environ["SLACK_TEAM_ID"],
    "OPENID_URL": "https://slack.com/openid/connect/keys",
}

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
