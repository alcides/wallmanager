import os
def relative(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = relative('db/dev.db') # Or path to database file if using sqlite3.
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''             # empty -> localhost
DATABASE_PORT = ''             # empty -> default
DATABASE_SUPPORTS_TRANSACTIONS = True

EMAIL_HOST = 'smtp.dei.uc.pt'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'no-reply@sensewall.dei.uc.pt'
DEFAULT_TO_EMAIL = 'wallmanager@dei.uc.pt'

SECRET_KEY = '%4)e8snda5-cewqsjx#%t$sg-j0txw)mb%leue1_^paa=(ft)e' # <------ Change this!

TIME_ZONE = 'Europe/Lisbon' # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
LANGUAGE_CODE = 'en-us' # http://www.i18nguy.com/unicode/language-identifiers.html
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = relative('media/')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

ROOT_URLCONF = 'webmanager.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'appman',
)

TEMPLATE_DIRS = (
    relative('templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'appman.middleware.swfupload.SWFUploadMiddleware',
    'appman.middleware.redirecter.Redirecter',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'appman.backends.StudentPopBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/applications/'

AUTH_LDAP_SERVER = "ldap://ldap3.dei.uc.pt"
AUTH_LDAP_USER_BASE = lambda email: "uid=%s,ou=%s,ou=People,dc=dei,dc=uc,dc=pt" % ( email.split("@")[0], 'student' in email and 'student' or 'eden' )
AUTH_LDAP_CERT = ""

WALL_APP_DIR = relative('../mtmenu/apps/')
ZIP_FOLDER = "applications"
ZIP_TEMP_FOLDER = "app_temp"

DEFAULT_CATEGORY = "Others"
APPS_MAX_LOG_ENTRIES = 3

LOG_FILENAME = relative('log.txt')

PROJECTOR_IPS = ('192.168.1.254', '192.168.1.253')
