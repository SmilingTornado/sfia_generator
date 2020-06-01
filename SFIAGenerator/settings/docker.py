from SFIAGenerator.settings.base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '18.132.14.148', 'sfia.worawat.com']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.getenv('DEBUG',True)) == 'True'
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB','postgres'),
        'USER': os.getenv('POSTGRES_USER','postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD','postgres2020'),
        'HOST': os.getenv('POSTGRES_HOST','db'),
        'PORT': os.getenv('POSTGRES_PORT','5432'),
    }
}