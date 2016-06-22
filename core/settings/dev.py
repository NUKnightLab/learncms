from .common import *

# This is an override of DEBUG in common.py which is set to default to False
# Do not do this in deployment. Instead, set DJANGO_DEBUG=True in the
# environment if you need to expose debugging info in deployment.
DEBUG = True
