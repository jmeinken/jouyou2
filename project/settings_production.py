from settings_global import *

LOGIN_URL = '/jouyou/login'
FORCE_SCRIPT_NAME = '/jouyou/'

STATIC_URL = '/jouyou/static/'

CSRF_COOKIE_NAME = 'jouyou_csrftoken'
SESSION_COOKIE_NAME = 'jouyou_sessionid'

DEBUG = True
ALLOWED_HOSTS = ['*']