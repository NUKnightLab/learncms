"""
Local Django settings for learncms project.

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
    os.path.normpath(os.path.join(PROJECT_ROOT, '../secrets/learncms/loc'))
)
from secrets import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
# extend base.py settings

WSGI_APPLICATION = 'conf.loc.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'learncms',
        'USER': 'learncms',
        'PASSWORD': 'default',
        'HOST': '127.0.0.1',
        'PORT': ''
    }
}


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# User uploads settings for S3
# In addition to below, set environment vars:
#
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
#
DEFAULT_FILE_STORAGE = 'learncms.admin.S3FileBrowserStorage'
from filebrowser.sites import site
site.directory = 'learncms'
from boto.s3.connection import OrdinaryCallingFormat
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
AWS_S3_URL_PROTOCOL = 'https'
AWS_S3_SECURE_URLS = False
AWS_STORAGE_BUCKET_NAME = 'media.knilab.com'
# not sure who uses this -- not S3BotoStorage
MEDIA_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)
# --- end S3 storages configuration ---
