import os
import sys
import platform
import djcelery

djcelery.setup_loader()

from django.contrib.messages import constants as messages

# ===========================
# = Directory Declaractions =
# ===========================

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR   = os.path.dirname(__file__)
TEMPLATE_DIRS = (os.path.join(CURRENT_DIR, 'templates'),)
MEDIA_ROOT    = os.path.join(CURRENT_DIR, 'media')
STATIC_ROOT   = os.path.join(CURRENT_DIR, 'static')
UTILS_ROOT    = os.path.join(CURRENT_DIR, 'utils')

# ==============
# = PYTHONPATH =
# ==============

if '/utils' not in ' '.join(sys.path):
    sys.path.append(UTILS_ROOT)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Tyler Rilling', 'tyler@underlost.net'))
MANAGERS = ADMINS

#DB info injected by Heroku
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

#Global Settings

BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_USER = "guest"
#BROKER_PASSWORD = "guest"
#BROKER_VHOST = "/"

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = "25"
#EMAIL_USE_TLS = True

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

AUTH_PROFILE_MODULE = 'accounts.Profile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = ()

WSGI_APPLICATION = 'bloop.wsgi.application'


# ===========================
# = Django-specific Modules =
# ===========================

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'bloop.urls'

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (

	#Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',

    #Prancing on Heroku
    'djcelery',
    'gunicorn',
    'south',
    
    #Internal
    'bloop.accounts',
    'bloop.blip',
    
)