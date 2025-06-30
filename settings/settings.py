import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-_rc#05r30b4x&d2%b20295aoggoz-*pxa7+gc*jx525@7ta55k#')

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*,9c31-41-90-188-61.ngrok-free.app,novel-definite-dodo.ngrok-free.app').split(',')

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'accounts',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    'django_browser_reload',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'django_otp.plugins.otp_email',
    'frontend',
    'channels',
    'corsheaders',
    "crispy_forms",
    'dashboard',
    'project',
    'task',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    "accounts.middleware.LastSeenMiddleware",
    "accounts.middleware.EnforceAdmin2FAMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

AUTH_USER_MODEL = 'accounts.CustomUser'

TAILWIND_APP_NAME = 'frontend'

TWO_FACTOR_REQUIRED_FOR_ADMIN = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://6b52-41-90-187-81.ngrok-free.app',
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

SITE_ID = 1
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_REDIRECT_URL = "/dashboard/"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"

DEFAULT_FROM_EMAIL=os.getenv('EMAIL_HOST_USER')

PAYMENT_EXPIRY_HOURS = 12

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "frontend/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings.context_processors.breadcrumbs',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

ASGI_APPLICATION = "settings.asgi.application"

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        },
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "key": os.getenv("GOOGLE_CLIENT_KEY", ""),
        }
    },
    "github": {
        "APP": {
            "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
            "secret": os.getenv("GITHUB_CLIENT_SECRET", ""),
        }
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'premium190.web-hosting.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')


# Mpesa Credentials
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_LIPA_SHORTCODE = os.getenv('MPESA_LIPA_SHORTCODE')
MPESA_LIPA_PASSWORD = os.getenv('MPESA_LIPA_PASSWORD')
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')

# Pesapal Credentials
PESAPAL_CONSUMER_KEY = os.getenv('PESAPAL_CONSUMER_KEY')
PESAPAL_CONSUMER_SECRET = os.getenv('PESAPAL_CONSUMER_SECRET')
PESAPAL_NOTIFICATION_ID = os.getenv('PESAPAL_NOTIFICATION_ID')

# InstantSend Credentials
INSTASEND_API_KEY = os.getenv('INSTASEND_API_KEY')
INSTASEND_API_KEY_PUBLIC = os.getenv('INSTASEND_API_KEY_PUBLIC')
INSTASEND_CALLBACK_URL = os.getenv('INSTASEND_CALLBACK_URL')


LOGGING = {
    "version": 1,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "webhook.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
