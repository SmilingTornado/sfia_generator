from SFIAGenerator.settings.base import *
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres2020',
        'HOST': 'db',
        'PORT': 5432,
    }
}