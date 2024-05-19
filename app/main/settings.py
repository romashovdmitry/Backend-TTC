# Python imports
from pathlib import Path
import os
import sys
from datetime import timedelta

# Telegram imports
from aiogram import Bot
from aiogram.enums import ParseMode

SECRET_KEY = os.getenv("SECRET_KEY") or "secret"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or ""
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition    

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # beatiful admin panel
    "adminlte3",
    # DRF
    "adrf",  # https://github.com/em1208/adrf
    # processing CORS errors
    "corsheaders",
    # Swagger
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # JWT
    "rest_framework_simplejwt",
    # my apps
    "main",
    "user",
    "club",
    "tournament",
    "telegram_bot"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # my middlewares
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "main.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'club_database_container',
        'PORT': os.getenv('POSTGRES_PORT')
    }
}

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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# my settings 👇

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    # swagger drf-spectacular
    'DEFAULT_SCHEMA_CLASS': 
        'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERERS': [
        'drf_spectacular.renderers.SpectacularRenderer',
        'rest_framework.renderers.JSONRenderer',
    ],
    # JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # auth
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated'
    ),
    # throttling
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day'
    }
}

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#settings
# default values are shown in example at link
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_LIFETIME"))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(os.getenv("REFRESH_TOKEN_LIFETIME"))
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": JWT_SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

CORS_ORIGIN_ALLOW_ALL = True

#CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:8000",]
#CORS_ALLOW_CREDENTIALS = True

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "user.authentication.CustomAuthenication"
]

HTTP_HEADERS = {
    "Access-Control-Allow-Origin": "https://localhost",
    "Access-Control-Allow-Credentials": True
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    # https://stackoverflow.com/a/67522312/24040439
    # https://drf-spectacular.readthedocs.io/en/latest/faq.html#filefield-imagefield-is-not-handled-properly-in-the-schema
    "COMPONENT_SPLIT_REQUEST": True

}


MEDIA_URL = os.getenv("MEDIA_URL")
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv("MEDIA_ROOT"))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(asctime)s %(levelname) -4s %(name) -2s [%(pathname)s:%(lineno)d] %(message)s"},
        "file": {"format": "%(asctime)s %(levelname) -4s %(name) -2s [%(filename)s:%(lineno)d] %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "filename": f"{BASE_DIR}/logs/django_log.log",
            "backupCount": 10,  # only 10 log files
            "maxBytes": 5242880,  # 5*1024*1024 bytes (5MB)
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}

bot = Bot(
    os.getenv("TELEGRAM_BOT_TOKEN"),
    parse_mode=ParseMode.HTML
)


if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }