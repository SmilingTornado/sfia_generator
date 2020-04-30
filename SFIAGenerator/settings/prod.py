from SFIAGenerator.settings.base import *
ALLOWED_HOSTS = ['18.130.244.39', 'sfia.worawat.com']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sfia',
        'USER': 'sfia_user',
        'PASSWORD': 'Cardiff2020',
        'HOST': 'localhost',
        'PORT': '',
    }
}