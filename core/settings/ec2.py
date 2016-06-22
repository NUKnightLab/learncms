from os import environ as env
# This has to go here b/c django is stoopid
SECRET_KEY = env['DJANGO_SECRET_KEY']

from .common import *
