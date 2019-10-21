from .settings import *

LOGIN_URL = '/kanji/login'
FORCE_SCRIPT_NAME = '/kanji/'

STATIC_URL = '/kanji/static/'

CSRF_COOKIE_NAME = 'kanji_csrftoken'
SESSION_COOKIE_NAME = 'kanji_sessionid'

DEBUG = True
ALLOWED_HOSTS = ['*']