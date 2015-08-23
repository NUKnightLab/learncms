"""
Staging Django settings for learncms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import os
import sys
from .base import *

# Import secrets

sys.path.append(
    os.path.normpath(os.path.join(PROJECT_ROOT, '../secrets/learncms/stg'))
)
from secrets import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ['learncms.knilab.com']


# Application definition
# extend base.py settings

WSGI_APPLICATION = 'conf.stg.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'learncms_stg',
        'USER': 'learncms',
        'PASSWORD': 'learncms',
        'HOST': 'rds-pgis.knilab.com',
        'PORT': '5432'
    }
}

# should these be in site.py?
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'knightlab@northwestern.edu')
# EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
# EMAIL_SUBJECT_PREFIX = '[learn.knightlab.com CMS] '
# EMAIL_USE_TLS = True
# SERVER_EMAIL = EMAIL_HOST_USER

# User uploads settings for S3
# In addition to below, set environment vars:
#
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
#
DEFAULT_FILE_STORAGE = 'learncms.admin.S3FileBrowserStorage'
from boto.s3.connection import OrdinaryCallingFormat
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
AWS_S3_URL_PROTOCOL = 'https'
AWS_S3_SECURE_URLS = False
AWS_STORAGE_BUCKET_NAME = 'media.knilab.com'
# not sure who uses this -- not S3BotoStorage
MEDIA_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)
# --- end S3 storages configuration ---

# Static files (CSS, JavaScript, Images)
# deployment to this location is managed by salt
STATIC_URL = '//{}/learncms/'.format(AWS_STORAGE_BUCKET_NAME)

#django-filebrowser needs its own storage
from django.core.files.storage import FileSystemStorage
FILEBROWSER_ROOT=os.path.normpath(os.path.join(PROJECT_ROOT,'../../learn-media'))
FILEBROWSER_URL="/fbimages/"
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

import os
try:
    os.makedirs(os.path.join(site.storage.location, site.directory))
    os.makedirs(os.path.join(site.storage.location, FILEBROWSER_VERSIONS_BASEDIR))
except Exception:
    pass
