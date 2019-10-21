from .settings_global import *



LOGIN_URL = '/login'

CSRF_COOKIE_NAME = 'dev_jouyou_csrftoken'
SESSION_COOKIE_NAME = 'dev_jouyou_sessionid'

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'kanji',
        'USER': 'kanji_site',
        'PASSWORD': 'CjDF3uRmy3b2VVVW',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


STATIC_ROOT = '/var/www/django_static/kanji/static/'