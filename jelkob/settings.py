"""
Django settings for Jelkob project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# We need to import it as alias so it is not processed by makemessages
from django.utils.translation import gettext_lazy as translate


# Load environment variables from .env file
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep the secret key secret
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or "0" * 50

# SECURITY WARNING: Disable debug mode in production
DEBUG = os.environ.get("DJANGO_DEBUG") == "1"

# SECURITY WARNING: Configure allowed hosts properly in production
ALLOWED_HOSTS = [host for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if host]

# SECURITY WARNING: Configure CORS origins properly in production
CORS_ALLOWED_ORIGINS = [host for host in os.environ.get("DJANGO_CORS_ORIGINS", "").split(",") if host]

# SECURITY WARNING: Configure CSRF origins properly in production
CSRF_TRUSTED_ORIGINS = [host for host in os.environ.get("DJANGO_CSRF_ORIGINS", "").split(",") if host]


# Application

INSTALLED_APPS = [
    # Daphne apps
    "daphne",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "django_filters",
    "django_eventstream",
    "rest_framework",
    "rest_framework.authtoken",
    "simple_history",
    "solo",
    "macros",
    "corsheaders",
    # Local apps
    "runner.apps.RunnerConfig",
    "editor.apps.EditorConfig",
    "frontend.apps.FrontendConfig",
]

MIDDLEWARE = [
    # CORS middlewares
    "corsheaders.middleware.CorsMiddleware",
    # Django middlewares
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Third-party middlewares
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "jelkob.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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

WSGI_APPLICATION = "jelkob.wsgi.application"
ASGI_APPLICATION = "jelkob.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE") or "django.db.backends.sqlite3",
        "NAME": os.environ.get("DATABASE_NAME") or BASE_DIR / "app.db",
        "HOST": os.environ.get("DATABASE_HOST", ""),
        "PORT": os.environ.get("DATABASE_PORT", ""),
        "USER": os.environ.get("DATABASE_USER", ""),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", ""),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Authentication
# https://docs.djangoproject.com/en/5.1/topics/auth/

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = None


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "sl"
TIME_ZONE = "Europe/Ljubljana"

USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("en", translate("English")),
    ("sl", translate("Slovene")),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "static/"


# Media files (uploads)
# https://docs.djangoproject.com/en/5.1/topics/files/

MEDIA_ROOT = BASE_DIR / "uploads"
MEDIA_URL = "uploads/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django REST framework

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "django_eventstream.renderers.SSEEventRenderer",
        "django_eventstream.renderers.BrowsableAPIEventStreamRenderer",
    ],
}


# Jelkob - Common

ROOT_URL = os.environ.get("ROOT_URL")
"""The full root URL of the application."""


# Jelkob - Editor

EDITOR_URL = os.environ.get("EDITOR_URL")
"""The full path to the editor website."""

EDITOR_ACTION = os.environ.get("EDITOR_ACTION") or "sandbox"
"""The action to perform in the editor."""


# Jelkob - Runner

RUNNER_URL = os.environ.get("RUNNER_URL")
"""The full path to the runner endpoint for running the patterns."""

RUNNER_TOKEN = os.environ.get("RUNNER_TOKEN")
"""The token to use for authenticating with the runner endpoint."""

INACTIVITY_PING_TIMEOUT = int(os.environ.get("INACTIVITY_PING_TIMEOUT") or 90)
"""How long to wait for a ping before considering the runner inactive."""

INACTIVITY_PATTERN_TIMEOUT = int(os.environ.get("INACTIVITY_PATTERN_TIMEOUT") or 30)
"""How long to wait after the pattern should have finished before considering the runner inactive."""


# Jelkob - Driver

DRIVER_URL = os.environ.get("DRIVER_URL")
"""The full path to the driver endpoint of the pattern content event stream."""


# Jelkob - Discord

DISCORD_USERNAME = os.environ.get("DISCORD_USERNAME") or "Jelkob"
"""The username to use for the Discord webhook."""

DISCORD_COLOR = int(os.environ.get("DISCORD_COLOR") or 5814783)
"""The color to use for the Discord embeds."""

DISCORD_AVATAR = os.environ.get("DISCORD_AVATAR")
"""The avatar to use for the Discord webhook."""

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
"""The webhook URL to use for sending messages to Discord."""
