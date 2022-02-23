from dotenv import load_dotenv
from pathlib import Path
import os


PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent
GLOBAL_DIR = BASE_DIR.parent

load_dotenv(BASE_DIR / ".env")


SECRET_KEY = os.getenv("SECRET_KEY")


DEBUG = False

ALLOWED_HOSTS = [
    "mydentist.uz",
    "www.mydentist.uz",
    "mydentist.pythonanywhere.com"
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appointment',
    'baseapp',
    'dentist',
    'dentx',
    'illness',
    'login',
    'mydentist',
    'notification',
    'patient'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mydentist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mydentist.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv("DATABASE_ENGINE"),
        'NAME': os.getenv("DATABASE_NAME"),
        'USER': os.getenv("DATABASE_USER"),
        'PASSWORD': os.getenv("DATABASE_PASSWORD"),
        'HOST': os.getenv("DATABASE_HOST"),
        'PORT': os.getenv("DATABASE_PORT"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'uz'

LANGUAGES = [
    ('uz', "O'zbek"),
    ('ru', "Русский")
]

EXTRA_LANGUAGES = [
    ('ru', "Русский")
]

LOCALE_PATHS = [
    PROJECT_DIR / 'locale'
]

TIME_ZONE = 'UTC'
TIME_ZONE_HOUR = 5

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = PROJECT_DIR / 'static'
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = GLOBAL_DIR / 'media'

LOGIN_URL = "/auth/login/"
LOGIN_URL_DENTX = "/dentx/auth/login/"

SESSION_EXPIRE_AT_BROWSER_CLOSE = False


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_SSL = True    # use port 465
EMAIL_USE_TLS = False    # use port 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
