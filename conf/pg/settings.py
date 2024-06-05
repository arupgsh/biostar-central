from biostar.forum.settings import *

# psql -U postgres -f create_db_and_user.sql

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_database',
        'USER': 'test_user',
        'PASSWORD': 'test_passwd',
        'HOST': 'localhost',  # Set to 'db' if using Docker
        'PORT': '5432',
    }
}
