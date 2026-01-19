import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = bool(os.environ.get("DEBUG", True))

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = (
    "painter",

    "django_extensions",

    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SECRET_KEY = "Django requires this to be set, but this project does not make use of it"

ROOT_URLCONF = "painter.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "painter.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default="postgres://localhost/painter",
    ),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

LANGUAGE_CODE = "en-gb"
USE_TZ = False

STATIC_ROOT = os.path.join(BASE_DIR, "painter/static")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")

# Imperial Painter settings
DEFAULT_IMPORTER = "painter.importers.import_cards"
GENERATORS = {
    "_test": {
        "key": "_test",
        "name": "Test cards",
    },
    "bfg": {
        "key": "bfg",
        "name": "Battlefleet Gothic",
    },
    "killteam": {
        "key": "killteam",
        "name": "Kill-Team",
    },
    "laundry": {
        "key": "laundry",
        "name": "The Laundry Files RPG",
        "importer": "painter.importers.import_laundry",
    },
    "little_pile_of_secrets": {
        "key": "little_pile_of_secrets",
        "name": "Little Pile of Secrets",
    },
    "ten_metres": {
        "key": "ten_metres",
        "name": "Ten Metres and Closing",
    },
    "murder_mystery": {
        "key": "murder_mystery",
        "name": "The Curse of Pendleton Manor",
    },
    "training_montage": {
        "key": "training_montage",
        "name": "Training Montage",
    },
    "wraithsight": {
        "key": "wraithsight",
        "name": "Wraithsight",
    },
}
