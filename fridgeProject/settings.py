"""
Django settings for fridgeProject project.

Generated by 'django-admin startproject' using Django 3.2.19.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import django_heroku
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2jrzbt&)mz(4w9*7a%sic2ovtwv^q5ah39eswx!zpmw_1lw8!9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#EMAILS CONFIGURATIONS.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'petrocrms@gmail.com'
EMAIL_HOST_PASSWORD = 'xcxtlxsqjwojythr'  #password for allowed for two-factor authentication..
EMAIL_USE_TLS = True   #for Gmail account.
# EMAIL_USE_SSL = False,   for secured connection.

ALLOWED_HOSTS = ["*"]

#django messages.... added.
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #installed apps.
    'uaa.apps.UaaConfig',
    'fridge.apps.FridgeConfig',
]

AUTH_USER_MODEL = 'uaa.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     # session settings
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

ROOT_URLCONF = 'fridgeProject.urls'

# session settings
# SESSION_EXPIRE_SECONDS = 300
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 5 # here the time is in mnutes
SESSION_TIMEOUT_REDIRECT = 'logout_url'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fridgeProject.wsgi.application'

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'sb.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ATOMIC_REQUESTS': False,
#         'AUTOCOMMIT': True,
#         'CONN_MAX_AGE': 0,
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'tipmdb',
#         'USER':'tipmcoder',
#         'PASSWORD': 'tipm@1',
#         'HOST':'localhost',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Dealing with static files...
STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
#dealing with media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

django_heroku.settings(locals())

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
