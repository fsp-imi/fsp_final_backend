from .settings import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'prod',
        'HOST': '213.171.9.104',
        'PORT': 3306,
        'USER': 'gen_user',
        'PASSWORD': 'hHZFlUgO$.M1hs',
    }
}