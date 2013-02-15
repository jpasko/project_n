# Used by Heroku to configure the database.
import dj_database_url
import os.path
PROJECT_ROOT = os.path.abspath('.')

DEBUG = False
DEV_SETTINGS = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('jpasko', 'jbpasko@gmail.com'),
)

# Declare the user profile module
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

MANAGERS = ADMINS

# Database config for Heroku
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# AWS settings.
AWS_STORAGE_BUCKET_NAME = 'citreous'
DEFAULT_FILE_STORAGE = 'project_n.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'project_n.s3utils.StaticRootS3BotoStorage'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME

ADMIN_MEDIA_PREFIX = 'http://s3.amazonaws.com/%s/admin/' % AWS_STORAGE_BUCKET_NAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '01x6wuntqa3w)l%wld#s#ce%dm96+ha3^$%l&amp;yf=@-px#r(lez'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project_n.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project_n.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'accounts',
    'portfolios',
    'imagekit',
    'storages',
    'zebra',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Names of the accounts.
FREE_ACCOUNT_NAME = 'basic'
PREMIUM_ACCOUNT_NAME = 'premium'
PROFESSIONAL_ACCOUNT_NAME = 'professional'

# The storage limits for free accounts
FREE_IMAGE_LIMIT = 20

# The storage limits for premium accounts
PREMIUM_IMAGE_LIMIT = 150

# The storage limits for professional accounts
PROFESSIONAL_IMAGE_LIMIT = 1000

# Redirect to this URL after login, and use request.user to redirect to the
# user's profile within the view.
LOGIN_REDIRECT_URL = '/accounts/profile/'

# Database configuration for Heroku
DATABASES['default'] = dj_database_url.config()

# Use the default Zebra app to interact with Stripe
ZEBRA_ENABLE_APP = True

# Use Zebra to extend the Customer model
ZEBRA_CUSTOMER_MODEL = 'accounts.models.Customer'

SQUARE_THUMBNAIL_DIMENSION = 250

WIDE_THUMBNAIL_WIDTH = 750

WIDE_THUMBNAIL_HEIGHT = 250

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_AUTO_THROTTLE = None

# Untracked local variables (secret keys and the like)
try:
    from locals import *
except:
    pass

# Use development settings locally
try:
   from dev_settings import *
except ImportError, e:
   pass
