# settings
# -*- coding: utf-8 -*-

import os, sys

# simplify absolute path generation
def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

#OAUTH_AUTH_VIEW = 'piston.authentication.oauth_auth_view'
#OAUTH_CALLBACK_VIEW = 'piston.authentication.oauth_user_auth'
OAUTH_CALLBACK_VIEW = 'api.views.request_token_ready'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# The python-django-piston will not install on Ubuntu, so
# after: hg clone https://bitbucket.org/jespern/django-piston
# make the installed 'piston' directory available here:
piston_installation_prefix = rel('..')

# make visible to python
sys.path.insert(0, piston_installation_prefix)

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = rel('posts.sqlite3')  # Or path to database file if using sqlite3.
#DATABASE_USER = ''             # Not used with sqlite3.
#DATABASE_PASSWORD = ''         # Not used with sqlite3.
#DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: '/home/media/media.lawrence.com/'
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: 'http://media.lawrence.com', 'http://example.com/media/'
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: 'http://foo.com/media/', '/media/'.
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'f@vhy8vuq7w70v=cnynm(am1__*zt##i2--i2p-021@-qgws%g'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'piston.middleware.ConditionalMiddlewareCompatProxy',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'piston.middleware.CommonMiddlewareCompatProxy',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    rel('templates'),
    rel('piston/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'piston',
    'blog',
    'api',
)

FIXTURE_DIRS = (
    rel('fixtures'),
)

APPEND_SLASH = False
