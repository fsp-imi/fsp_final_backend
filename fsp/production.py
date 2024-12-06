from django.conf import settings

settings.DEBUG = False

settings.ALLOWED_HOSTS = ['fsp-imi-fsp-final-backend-5a76.twc1.net', 'localhost', '127.0.0.1']

settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'prod',
        'HOST': '213.171.9.104',
        'PORT': 3306,
        'USER': 'gen_user',
        'PASSWORD': 'hHZFlUgO$.M1hs',
    }
}