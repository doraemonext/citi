"""Common settings and globals."""


import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path
from logging.handlers import SysLogHandler


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Doraemonext', 'doraemonext@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Asia/Shanghai'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'zh-cn'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"k!i33q!h2ai32$q_+-4l01+pej3q2s$-kwxx$tv0y35xph-gmz"
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Useful template tags:
    # 'django.contrib.humanize',

    'annoying',
    'mptt',
    'django_mptt_admin',
    'rest_framework',
    'captcha',
    'registration',

    'system.users',
    'system.authtoken',

    'apps.account',
    'apps.log',
    'apps.location',
    'apps.fund',
    'apps.crowdfunding',
    'apps.question',
)

# Apps specific for this project go here.
LOCAL_APPS = (
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(pathname)s:%(funcName)s:%(lineno)d] [%(threadName)s:%(thread)d] [%(name)s] [%(levelname)s] - %(message)s'
        },
    },
    'handlers': {
        "apps_account_handles": {
            'level': 'DEBUG',
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            'filename': os.path.join(SITE_ROOT, 'logs/apps_account.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        "apps_crowdfunding_handles": {
            'level': 'DEBUG',
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            'filename': os.path.join(SITE_ROOT, 'logs/apps_crowdfunding.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        "apps_fund_handles": {
            'level': 'DEBUG',
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            'filename': os.path.join(SITE_ROOT, 'logs/apps_fund.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        "apps_location_handles": {
            'level': 'DEBUG',
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            'filename': os.path.join(SITE_ROOT, 'logs/apps_location.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        "apps_log_handles": {
            'level': 'DEBUG',
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            'filename': os.path.join(SITE_ROOT, 'logs/apps_log.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        "apps_question_handles": {
            'level': 'DEBUG',
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            'filename': os.path.join(SITE_ROOT, 'logs/apps_question.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        "system_users_handles": {
            'level': 'DEBUG',
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            'filename': os.path.join(SITE_ROOT, 'logs/system_users.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        "system_authtoken_handles": {
            'level': 'DEBUG',
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            'filename': os.path.join(SITE_ROOT, 'logs/system_authtoken.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
    },
    'loggers': {
        "apps.account": {
            "handlers": ["apps_account_handles"],
            "level": "DEBUG",
        },
        "apps.crowdfunding": {
            "handlers": ["apps_crowdfunding_handles"],
            "level": "DEBUG",
        },
        "apps.fund": {
            "handlers": ["apps_fund_handles"],
            "level": "DEBUG",
        },
        "apps.location": {
            "handlers": ["apps_location_handles"],
            "level": "DEBUG",
        },
        "apps.log": {
            "handlers": ["apps_log_handles"],
            "level": "DEBUG",
        },
        "apps.question": {
            "handlers": ["apps_question_handles"],
            "level": "DEBUG",
        },
        "system.users": {
            "handlers": ["system_users_handles"],
            "level": "DEBUG",
        },
        "system.authtoken": {
            "handlers": ["system_authtoken_handles"],
            "level": "DEBUG",
        }
    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
########## END WSGI CONFIGURATION


########## SOUTH CONFIGURATION
# See: http://south.readthedocs.org/en/latest/installation.html#configuring-your-django-installation
INSTALLED_APPS += (
    # Database migration helpers:
    'south',
)
# Don't need to use South when setting up a test database.
SOUTH_TESTS_MIGRATE = False
########## END SOUTH CONFIGURATION


########## FILE UPLOAD CONFIGURATION
UPLOAD_CROWDFUNDING_PROJECT_COVER = 'crowdfunding/project/cover'
UPLOAD_CROWDFUNDING_PROJECT_FEEDBACK = 'crowdfunding/project/feedback'
########## END UPLOAD CONFIGURATION


########## REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'system.authtoken.authentication.ExpiringTokenAuthentication',
    )
}
AUTHTOKEN_EXPIRE_SECOND = 7
########## END REST FRAMEWORK CONFIGURATION

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/accounts/profile/'

EMAIL_FROM = 'doraemonext@gmail.com'

ACCOUNT_ACTIVATION_DAYS = 7

ATOMIC_REQUESTS = True