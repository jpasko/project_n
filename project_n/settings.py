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
AWS_STORAGE_BUCKET_NAME = 'folio24'
DEFAULT_FILE_STORAGE = 'project_n.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'project_n.s3utils.StaticRootS3BotoStorage'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'https://s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME

ADMIN_MEDIA_PREFIX = 'https://s3.amazonaws.com/%s/admin/' % AWS_STORAGE_BUCKET_NAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'https://s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME

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
    # 'django.template.loaders.eggs.Loader',
)

# List of template context processors.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'context_processors.custom.domain',
    'context_processors.custom.thumbnail_dimensions',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'middleware.custom.SubdomainURLs',
    'middleware.custom.ParseURLs',
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
FREE_IMAGE_LIMIT = 35

# The storage limits for premium accounts
PREMIUM_IMAGE_LIMIT = 500

# The storage limits for professional accounts
PROFESSIONAL_IMAGE_LIMIT = 1500

# Redirect to this URL after login, and use request.user to redirect to the
# user's profile within the view.
LOGIN_REDIRECT_URL = '/accounts/profile/'

# Database configuration for Heroku
DATABASES['default'] = dj_database_url.config()

# Use the default Zebra app to interact with Stripe
ZEBRA_ENABLE_APP = True

# Use Zebra to extend the Customer model
ZEBRA_CUSTOMER_MODEL = 'accounts.models.Customer'

# Image dimensions
GALLERY_THUMBNAIL_DIMENSION = 100
IMAGE_WIDTH = 940
IMAGE_HEIGHT = 940
THUMBNAIL_WIDTH = 500
THUMBNAIL_HEIGHT = 500

EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = 'support@folio24.com'
AWS_SES_AUTO_THROTTLE = None

# [TEST] Stripe publishable API key
STRIPE_PUBLISHABLE = 'pk_test_dyJgXQH2KaYvS3jBYyVRdJa5'

# Allow user sessions to exist across subdomains
SESSION_COOKIE_DOMAIN = '.folio24.com'

# The domain name to use in templates.
DOMAIN = 'folio24.com'

# The different URLs to use for the main content and the user subdomains.
MAIN_URLS = 'project_n.urls'
USER_URLS = 'project_n.user_urls'

# A list of reserved terms.
# RESERVED_TERMS = ['login', 'accounts', 'register', 'logout', 'welcome',
#                  'password_change', 'delete', 'privacy', 'terms', 'spindrift',
#                  'admin', 'reorder_galleries', 'reorder_photos', 'about',
#                  'contact', 'None', 'domains', 'invalid']
RESERVED_TERMS = ['domains', 'invalid']

# Custom backend to allow users to log in with their email addresses as well.
# Requires that email addresses uniquely identify a user.
AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Grab some settings from config vars in the prod environment.
try:
    STRIPE_SECRET = os.environ['STRIPE_SECRET']
    STRIPE_PUBLISHABLE = os.environ['STRIPE_PUBLISHABLE']
except:
    pass

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
