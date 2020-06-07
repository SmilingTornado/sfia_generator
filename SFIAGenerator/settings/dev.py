from SFIAGenerator.settings.base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

CSRF_TRUSTED_ORIGINS = ['localhost', '127.0.0.1', '0.0.0.0']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}
