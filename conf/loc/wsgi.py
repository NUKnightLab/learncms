import os
from os.path import abspath, dirname, join
import sys

project_dir = dirname(dirname(dirname(abspath(__file__))))

virtualenv_dir =  join(os.environ['WORKON_HOME'], 
    'cityhallmonitor/lib/python2.7/site-packages')

sys.path.append(project_dir)
sys.path.append(virtualenv_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.loc")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here