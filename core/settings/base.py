"""
Common Django settings for learncms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from os.path import abspath, dirname, join, normpath


CORE_ROOT = dirname(dirname(abspath(__file__)))

PROJECT_ROOT = dirname(CORE_ROOT)

# Application definition
# See also per-deployment target settings for
# STATIC_URL
# STATICFILES_STORAGE
# Don't change this, it is connected to our salt deployment system
STATIC_ROOT = '/tmp/learncms-static'

STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
)

MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'uploads'))

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/uploads/'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

FIXTURE_DIRS = (
    join(PROJECT_ROOT, 'fixtures'),
)

ADMINS = (
    ('Knight Lab', 'knightlab@northwestern.edu'),
)

MANAGERS = ADMINS

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'learncms',
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

GRAPPELLI_ADMIN_TITLE = 'Learn.KnightLab.com'

# boring standard stuff
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FILEBROWSER_DEFAULT_SORTING_BY = 'name'
