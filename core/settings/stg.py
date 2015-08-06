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
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
from boto.s3.connection import OrdinaryCallingFormat 
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
AWS_STORAGE_BUCKET_NAME = 'media.knilab.com'
MEDIA_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)
AWS_S3_SECURE_URLS = False
# --- end S3 storages configuration ---

# Static files (CSS, JavaScript, Images)
# deployment to this location is managed by salt
STATIC_URL = '//{}/learncms/'.format(AWS_STORAGE_BUCKET_NAME)
