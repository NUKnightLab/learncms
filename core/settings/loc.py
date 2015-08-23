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

#django-filebrowser needs its own storage
from django.core.files.storage import FileSystemStorage
FILEBROWSER_ROOT=os.path.normpath(os.path.join(PROJECT_ROOT, 'fbimages'))
FILEBROWSER_URL="/fbimages/"
FILEBROWSER_STORAGE = FileSystemStorage(location=FILEBROWSER_ROOT,base_url=FILEBROWSER_URL)
from filebrowser.sites import site
site.storage = FILEBROWSER_STORAGE
site.directory = ''
import os
try:
    os.makedirs(os.path.join(site.storage.location, site.directory))
except FileExistsError:
    pass
