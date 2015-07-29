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


# Static files (CSS, JavaScript, Images)
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_URL = '//media.knilab.com/learncms/'
