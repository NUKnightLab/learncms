"""
Django settings docs:
https://docs.djangoproject.com/en/1.8/topics/settings/
https://docs.djangoproject.com/en/1.8/ref/settings/

*** DEVELOPER NOTES ***

For DEBUG mode in deploymnet set DJANGO_DEBUG=True in the environment
variables instead of setting DEBUG=True in the settings files.
"""
import os
from os.path import abspath, dirname, join
from os import environ as env

PROJECT_NAME = env['PROJECT_NAME']
CORE_ROOT = dirname(dirname(abspath(__file__)))
PROJECT_ROOT = dirname(CORE_ROOT)

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'learncms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    'reversion'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': env['DB_ENGINE__DEFAULT'],
        'NAME': env['DB_NAME__DEFAULT'],
        'USER': env['DB_USER__DEFAULT'],
        'PASSWORD': env['DB_PASSWORD__DEFAULT'],
        'HOST': env['DB_HOST__DEFAULT'],
        'PORT': env['DB_PORT__DEFAULT']
    }
}

# ~~ everything below here is pretty standard and should not need to be edited ~~

ADMINS = (
    ('Knight Lab', 'knightlab@northwestern.edu'),
)
MANAGERS = ADMINS


# SECURITY WARNING: don't run with debug turned on in production!
# Avoid changing DEBUG here. Instead use the --debug manage.py flag, or
# set the environment variable DJANGO_DEBUG=True
DEBUG = True if env.get('DJANGO_DEBUG', '').lower() == 'true' else False

ALLOWED_HOSTS = env['APPLICATION_DOMAINS'].split(',')
WSGI_APPLICATION = 'core.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# static

# Static hosted in S3, thus STATIC_ROOT only used for collectstatic
STATIC_ROOT = env['STATIC_TMPDIR']
STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
)
STATIC_URL = env['STATIC_URL']

FIXTURE_DIRS = (
    join(PROJECT_ROOT, 'fixtures'),
)

#MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'uploads'))

ROOT_URLCONF = 'learncms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.core.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]


MEDIA_URL = '/uploads/'
# User uploads settings for S3
# In addition to below, set environment vars:
#
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
#
# dev
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# prd  not sure why the difference btwn this and stg.
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
from boto.s3.connection import OrdinaryCallingFormat
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
AWS_S3_URL_PROTOCOL = 'https'
AWS_S3_SECURE_URLS = False
AWS_STORAGE_BUCKET_NAME = env['AWS_STORAGE_BUCKET_NAME']

# not sure this is needed with the new TEMPLATES structure
#TEMPLATE_DIRS = (
#    join(PROJECT_ROOT, 'templates'),
#)

GRAPPELLI_ADMIN_TITLE = 'Learn.KnightLab.com'
FILEBROWSER_DEFAULT_SORTING_BY = 'name'

URL_ROOT = env['URL_ROOT'] # used for OG & twitter cards, etc

# not sure who uses this -- not S3BotoStorage
# MEDIA_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)

# Static files (CSS, JavaScript, Images)
# deployment to this location is managed by salt
#STATIC_URL = '//{}/learncms/'.format(AWS_STORAGE_BUCKET_NAME)

#django-filebrowser needs its own storage
from django.core.files.storage import FileSystemStorage
FILEBROWSER_ROOT=os.path.normpath(os.path.join(PROJECT_ROOT,'../../learn-media'))
FILEBROWSER_URL="/imagelib/"
FILEBROWSER_STORAGE = FileSystemStorage(location=FILEBROWSER_ROOT,base_url=FILEBROWSER_URL)
from filebrowser.sites import site
site.storage = FILEBROWSER_STORAGE
# site.directory needs to end with a slash
site.directory = 'uploads/'
FILEBROWSER_VERSIONS_BASEDIR = '_versions/' # this doesn't seem to work?
FILEBROWSER_VERSIONS = { # this doesn't seem to work?
    'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop'},
    # 'thumbnail': {'verbose_name': 'Thumbnail (1 col)', 'width': 60, 'height': 60, 'opts': 'crop'},
    # 'small': {'verbose_name': 'Small (2 col)', 'width': 140, 'height': '', 'opts': ''},
    # 'medium': {'verbose_name': 'Medium (4col )', 'width': 300, 'height': '', 'opts': ''},
    # 'big': {'verbose_name': 'Big (6 col)', 'width': 460, 'height': '', 'opts': ''},
    # 'large': {'verbose_name': 'Large (8 col)', 'width': 680, 'height': '', 'opts': ''},
}

try:
    os.makedirs(os.path.join(site.storage.location, site.directory))
    os.makedirs(os.path.join(site.storage.location, FILEBROWSER_VERSIONS_BASEDIR))
except Exception:
    pass
