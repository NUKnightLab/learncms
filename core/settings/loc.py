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
# site.directory needs to end with a slash
site.directory = 'uploads/'
FILEBROWSER_VERSIONS_BASEDIR = '_versions/'
FILEBROWSER_VERSIONS = {
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
except FileExistsError:
    pass
