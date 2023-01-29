import os
from pathlib import Path

from django.utils.encoding import force_str
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = force_str(os.getenv('SECRET_KEY'))

DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'sorl.thumbnail',
    'debug_toolbar',
    'admin_panel.apps.AdminPanelConfig',
    'orders.apps.OrdersConfig',
    'cart.apps.CartConfig',
    'users.apps.UsersConfig',
    'items.apps.ItemsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'dom_u_gnoma.urls'

TEMPLATES_DIR = BASE_DIR.joinpath('templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'dom_u_gnoma.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': force_str(os.getenv('ENGINE')),
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': force_str(os.getenv('USER')),
        'PASSWORD': force_str(os.getenv('PASSWORD'))
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

STATICFILES_DIRS = [BASE_DIR.joinpath('static')]
STATIC_URL = '/static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# Настройки для отправки писем
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = force_str(os.getenv('EMAIL_HOST'))
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = force_str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = force_str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = force_str(os.getenv('DEFAULT_FROM_EMAIL'))

# Настройки аутентификации
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SESSION_CART = 'cart'  # Корзина, доступна так же для анонимов
