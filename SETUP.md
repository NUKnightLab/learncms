### Local development setup

Prereqs:

* Python 3.4.x
* Postgres 9.3.x
* a virtual environment with the python dependencies installed
* an initialized database

Once you can check all four of these off, you should be able to run the CMS locally and make and test changes to the code.

If you only want to work on the web components, all you need is something to work as a local web server.

#### Install Python 3.4.4

Download installer from https://www.python.org/downloads/release/python-343/

**OR**

Install using [Homebrew](http://brew.sh):

`brew install python3`

**Note**: Whichver of the above you chose, you may need to upgrade virtualenvwrapper.

`sudo pip install virtualenvwrapper --upgrade`

#### Install PostgreSQL

Download and run installer for Mac OS X Version 9.3.9

http://www.enterprisedb.com/products-services-training/pgdownload

    Default installation directory = /Library/PostgreSQL/9.3
    Default data directory /Library/PostgreSQL/9.3/data
    Default Port = 5432
    Use default locale

Add the PostgreSQL bin directory to your PATH environment variable:

`PATH=$PATH:/Library/PostgreSQL/9.3/bin`

You may need to add the PostgreSQL lib directory to your DYLD_FALLBACK_LIBRARY_PATH environment variable:

`DYLD_FALLBACK_LIBRARY_PATH=$DYLD_FALLBACK_LIBRARY_PATH:/Library/PostgreSQL/9.3/lib`

**or**

Install using [Homebrew](http://brew.sh):

`brew install postgres --with-python`

(I installed Postgres with homebrew a long time ago, so can't verify this exact command.)

#### Setup PostgreSQL


Create the `learncms` database and `learncms` user by executing the `initdb.sh` script.

`$ ./initdb.sh`

This script assumes you've created a Postgres admin user with the same username as your shell login. If that's not the case, use this form instead:

`$ PGUSER="postgres" ./initdb.sh`

If your Postgres admin user has a different name, change the value of `PGUSER`.


Verify you can connect to database as learncms user:

```
$ psql -U learncms learncms
```

#### Setup project

If you just installed Python 3, you may need to upgrade `virtualenvwrapper` (see [SETUP.md](SETUP.md))
Make virtual environment and install requirements:

```
$ mkvirtualenv --python=/usr/local/bin/python3 learn-cms
$ pip install -r requirements.txt
$ export DJANGO_SETTINGS_MODULE='core.settings.loc'
$ cat >> ${VIRTUAL_ENV}/bin/postactivate <<END

export DJANGO_SETTINGS_MODULE='core.settings.loc'
echo "DJANGO_SETTINGS_MODULE set to \$DJANGO_SETTINGS_MODULE"

END

```

Have Django do its basic setup

```
python manage.py collectstatic
python manage.py migrate
python manage.py createsuperuser
```

Now you should be able to run the server:

    python manage.py runserver

Go to `http://localhost:8000` and you should see a message that there are no lessons. Go to
`http://localhost:8000/admin/` and log in as the user you created with `createsuperuser` and
you can start adding some!
