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
    os.path.normpath(os.path.join(PROJECT_ROOT, '../secrets/learncms/prd'))
)
from secrets import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ['learncms.knightlab.com']


# Application definition
# extend base.py settings

WSGI_APPLICATION = 'conf.prd.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'learncms_prd',
        'USER': 'learncms',
        'PASSWORD': 'learncms',
        'HOST': 'rds-pgis.knilab.com',
        'PORT': '5432'
    }
}

# User uploads settings for S3
# In addition to below, set environment vars:
#
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
#
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
from boto.s3.connection import OrdinaryCallingFormat 
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
AWS_STORAGE_BUCKET_NAME = 'media.knightlab.com'
MEDIA_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)
AWS_S3_SECURE_URLS = False
# --- end S3 storages configuration ---



# Static files (CSS, JavaScript, Images)
# deployment to this location is managed by salt
STATIC_URL = '//{}/learncms/'.format(AWS_STORAGE_BUCKET_NAME)
