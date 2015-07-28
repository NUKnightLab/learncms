### Local development setup

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

