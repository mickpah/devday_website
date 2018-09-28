"""
Django settings for devday project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/

Please keep this list of settings sorted alphabetically!

"""
import os
import mimetypes
from requests import get

from django.core.exceptions import ImproperlyConfigured


def gettext(s):
    return s


def get_env_variable(var_name):
    """
    Get a setting from an environment variable.

    :param str var_name: variable name

    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

_VAULT_DATA = None
_VAULT_URL = vault_url = "{}/v1/secret/data/devday".format(
    get_env_variable('VAULT_URL'))


def _fetch_from_vault():
    global _VAULT_DATA
    if not _VAULT_DATA:
        r = get(_VAULT_URL,
                headers={'x-vault-token': get_env_variable('VAULT_TOKEN')})
        r.raise_for_status()
        _VAULT_DATA = r.json()['data']['data']
    return _VAULT_DATA


def get_vault_variable(var_name):
    """
    Get a setting from vault

    :param var_name: variable name
    :return: variable data from vault /secret/data/devday
    """
    try:
        return _fetch_from_vault()[var_name]
    except KeyError:
        error_msg = "Define %s in Vault key at %s" % (var_name, _VAULT_URL)
        raise ImproperlyConfigured(error_msg)


def get_variable_cascade(var_name, type=str, default_value=None):
    """
    Try to get a setting from Vault or the environment and fallback to
    default_value if it is defined.

    Variables are transformed to uppercase before they are looked up in the
    environment.

    If no default is defined and the variable cannot be found in either
    Vault or the environment an ImproperlyConfigured exception is raised.

    :param var_name: variable name
    :param type: result type
    :param default_value: default value
    :return: variable from Vault or the environment
    """
    try:
        value = _fetch_from_vault()[var_name]
    except KeyError:
        try:
            value = os.environ[var_name.upper()]
        except KeyError:
            if default_value is None:
                error_msg = ('Define %s in Vault key at %s or set the'
                             ' environment variable %s') % (
                    var_name, _VAULT_URL, var_name.upper()
                )
                raise ImproperlyConfigured(error_msg)
            else:
                return default_value
    try:
        return type(value)
    except ValueError:
        raise ImproperlyConfigured(
            'Cannot interpret value %s as %s', value, type.__name__)


mimetypes.add_type("image/svg+xml", ".svg", True)

# settings for django-registration
# see: https://django-registration.readthedocs.io/en/2.1.1/index.html
ACCOUNT_ACTIVATION_DAYS = 14
ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'attendee.devdayuser'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

CMS_LANGUAGES = {
    1: [
        {
            'code': 'de',
            'name': gettext('de'),
            'public': True,
            'hide_untranslated': False,
            'redirect_on_fallback': True,
        },
    ],
    'default': {
        'fallbacks': ['de'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}
CMS_PLACEHOLDER_CONF = {}
CMS_STYLE_NAMES = (
    # styles for bootstrap grid model
    ('row', gettext('row')),
    ('container', gettext('container')),
    ('col-xs-12', gettext('col-xs-12')),
    ('col-md-12', gettext('col-md-12')),
)
CMS_TEMPLATES = (
    ('devday.html', 'Devday'),
    ('devday_index.html', 'Dev Day Startseite'),
)
CMS_PERMISSION = True
CRISPY_TEMPLATE_PACK = 'bootstrap3'

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_variable_cascade('DEVDAY_PG_DBNAME'),
        'USER': get_variable_cascade('DEVDAY_PG_USER'),
        'PASSWORD': get_variable_cascade('postgresql_password'),
        'HOST': get_variable_cascade('DEVDAY_PG_HOST'),
        'PORT': get_variable_cascade('DEVDAY_PG_PORT'),
    }
}
DEBUG = False
DEVDAY_FACEBOOK_URL = 'https://www.facebook.com/events/193156441425350/'
DEVDAY_TWITTER_URL = 'https://twitter.com/devdaydresden'
DEVDAY_XING_URL = 'https://www.xing.com/events/dev-day-2018-1897927'

EVENT_ID = 2

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'devday',
    'event.apps.EventsConfig',
    'attendee.apps.AttendeeConfig',
    'talk.apps.SessionsConfig',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'easy_thumbnails',
    'filer',
    'djangocms_text_ckeditor',
    'djangocms_style',
    'djangocms_column',
    'djangocms_file',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'reversion',
    'crispy_forms',
    'django_file_form',
    'django_file_form.ajaxuploader',
    'twitterfeed',
]

LANGUAGE_CODE = 'de'
LANGUAGES = (
    ('de', gettext('de')),
)

MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
MEDIA_URL = '/media/'
MIDDLEWARE_CLASSES = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]
MIGRATION_MODULES = {}

REGISTRATION_OPEN = get_variable_cascade('registration_open', bool, True)
ROOT_URLCONF = 'devday.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_vault_variable('secret_key')

SPONSORING_OPEN = get_variable_cascade('sponsoring_open', bool, False)

SITE_ID = 1
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'devday', 'static'),
)

TALK_PUBLIC_SPEAKER_IMAGE_HEIGHT = 960
TALK_PUBLIC_SPEAKER_IMAGE_WIDTH = 636
TALK_SUBMISSION_OPEN = get_variable_cascade('talk_submission_open', bool, True)
TALK_THUMBNAIL_HEIGHT = 320
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'devday', 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
                'devday.contextprocessors.devdaysettings_contextprocessor',
                'talk.context_processors.committee_member_context_processor',
                'twitterfeed.contextprocessors.twitter_feed_context_processor',
                'event.contextprocessors.current_event_contextprocessor',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ],
        },
    },
]
TIME_ZONE = 'Europe/Berlin'
TWITTERFEED_PROXIES = {}
TWITTERFEED_PATHS = ['/']

USE_I18N = True
USE_L10N = True
USE_TZ = True
