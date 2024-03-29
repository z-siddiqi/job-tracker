from pathlib import Path
from environs import Env

from django.core.management.utils import get_random_secret_key

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = [
    "job-tracker.zainuddinsiddiqi.com",
    "192.241.140.13",
    "localhost",
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local
    "accounts.apps.AccountsConfig",
    "boards.apps.BoardsConfig",
    "pages.apps.PagesConfig",
    "tasks.apps.TasksConfig",
    "metrics.apps.MetricsConfig",
    "summernote.apps.SummernoteConfig",
    # 3rd party
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap5",
    "chartjs",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR.joinpath("templates"))],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


#  Primary key type

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Static files

STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR.joinpath("static"))]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# User model

AUTH_USER_MODEL = "accounts.CustomUser"


# django-crispy-forms

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Urls

ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")
LOGIN_REDIRECT_URL = "board_list"
LOGOUT_REDIRECT_URL = "home"
