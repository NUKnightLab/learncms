# learn.knightlab.com CMS

Learn.knightlab.com is a website created by students, for students, to help develop web making skills.

# Developing the CMS

## Prereqs
If you are going to work on developing the CMS, you need to have installed Python 3 and Postgres 9.x. See [SETUP.md](SETUP.md) for details.

#### Setup project

If you just installed Python 3, you may need to upgrade `virtualenvwrapper` (see [SETUP.md](SETUP.md))
Make virtual environment and install requirements:

```
$ mkvirtualenv --python=/usr/local/bin/python3 learn-cms
$ pip install -r requirements.txt
$ cat >> ${VIRTUAL_ENV}/bin/postactivate <<END

export DJANGO_SETTINGS_MODULE='core.settings.loc'
echo "DJANGO_SETTINGS_MODULE set to $DJANGO_SETTINGS_MODULE"

END

```

Create database tables:

```
python manage.py migrate
```

