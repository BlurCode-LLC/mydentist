from decouple import config, Csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent
GLOBAL_DIR = BASE_DIR.parent


SECRET_KEY = config('SECRET_KEY')


DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# ALLOWED_HOSTS = [
#     "mydentist.uz",
#     "www.mydentist.uz",
#     "mydentist.pythonanywhere.com"
# ]

APPEND_SLASH = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework_swagger',
    'appointment',
    'api',
    'baseapp',
    'bot',
    'dentist',
    'dentx',
    'illness',
    'login',
    'mydentist',
    'notification',
    'patient'
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'mydentist.handler.LanguageMiddleware'
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

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
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
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
    ('en', "English"),
    ('ru', "Русский")
]

EXTRA_LANGUAGES = [
    ('en', "English"),
    ('ru', "Русский"),
]

LOCALE_PATHS = [
    PROJECT_DIR / 'locale'
]

TIME_ZONE = 'UTC'
TIME_ZONE_HOUR = 5

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC_ROOT = PROJECT_DIR / 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    PROJECT_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_DIR / 'media'

LOGIN_URL = "/auth/login/"
LOGIN_URL_DENTX = "/dentx/auth/login/"

SESSION_EXPIRE_AT_BROWSER_CLOSE = False


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_SSL = False    # use port 465
EMAIL_USE_TLS = True    # use port 587
# EMAIL_SSL_CERTFILE = BASE_DIR / 'ssl/fullchain.pem'
# EMAIL_SSL_KEYFILE = BASE_DIR / 'ssl/privkey.pem'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')

FIXTURES_DIRS = [
    BASE_DIR / 'baseapp',
    BASE_DIR / 'dentist',
    BASE_DIR / 'illness',
    BASE_DIR / 'mydentist',
    BASE_DIR / 'patient',
]

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         }
#     },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_false'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'propagate': True,
#         }
#     }
# }
