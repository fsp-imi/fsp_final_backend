"""
Django settings for fsp project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-rm3u8+1f8f5)^(*w%i-5k3@$z83u)l%w-qq!^4f+xk%voxxhr='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['fsp-imi-fsp-final-backend-5a76.twc1.net', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['http://localhost', 'https://fsp-imi-fsp-final-backend-5a76.twc1.net', 'http://127.0.0.1']

CORS_ALLOW_HEADERS = ['Api-Key']

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'DELETE',
    'PUT',
    'PATCH',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'corsheaders',
    'users',
    'country',
    'contests',
    'notifications',
    'subscription',
    'federations',
    'claims',
    'contestant',
    'results',
    'storages',
    's3',
    'analytics',
    "rest_framework_api_key",
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.AllowAny',
        'rest_framework_api_key.permissions.HasAPIKey',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'EXCEPTION_HANDLER': 'fsp.utils.custom_exception_handler.custom_exception_handler',
}

API_KEY_CUSTOM_HEADER = "HTTP_API_KEY"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fsp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'fsp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'  
MEDIA_URL = 'media/'

# S3 Config

AWS_ACCESS_KEY_ID = "G61YKZWAGWETW1943815"
AWS_SECRET_ACCESS_KEY = "B0BxNcwkCTRzPGgDOa8hSSAnB1tD7r8Pjp5Kj1vn"
AWS_STORAGE_BUCKET_NAME = "594bf291-b139f3af-5d47-443a-84d1-f756636511a8"
AWS_S3_ENDPOINT_URL = "https://s3.timeweb.cloud"  # URL вашего S3-хранилища
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

STORAGES = {

    # Media file (image) management  
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
   
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Confirm reg mail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.timeweb.ru'
EMAIL_PORT = 2525  # Если используется SSL
EMAIL_USE_SSL = False  # Используем SSL
# EMAIL_USE_TLS = True  # Если используется TLS (и тогда порт 587)
EMAIL_USE_LOCALTIME = True
EMAIL_HOST_USER = 'info@beercut.ru'  # Ваш email-адрес
EMAIL_HOST_PASSWORD = 'iefyewbxp5'  # Пароль от email
DEFAULT_FROM_EMAIL = 'info@beercut.ru'

LOGIN_REDIRECT_URL = '/login/'

LOGIN_URL = '/login/'

LOGIN_EXEMPT_URLS = (
    r'^auth/password_reset',
    r'^auth/password_reset/done',
    r'^auth/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
    r'^auth/reset/complete',
)