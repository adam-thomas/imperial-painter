import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = bool(os.environ.get("DEBUG", True))

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = (
    "painter",
    "test_app",

    "django_extensions",

    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

SECRET_KEY = "Django requires this to be set, but this project does not make use of it"

ROOT_URLCONF = "test_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "test_app.wsgi.application"

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

TEST_RUNNER = "painter.tests.runner.TestRunner"

# Imperial Painter settings
DEFAULT_IMPORTER = "painter.importers.import_cards"
GENERATORS = {
    "_test": {
        "key": "_test",
        "name": "Test cards",
        # "hidden": True,
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
    # TODO
}
