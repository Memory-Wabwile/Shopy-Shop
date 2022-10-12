import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shopyshop',
        'USER': 'memory',
        'PASSWORD': 'MEMory',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
