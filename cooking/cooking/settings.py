"""
Django settings for cooking project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from unipath import Path 
BASE_DIR = Path(__file__).ancestor(2)

TEMPLATE_DIRS = (
    BASE_DIR.child('templates'),
    BASE_DIR.child('image'),
    )

STATICFILES_DIRS = (
    BASE_DIR.child('static'),
    BASE_DIR.child('media'),
    )


##TEMPLATE_CONTEXT_PROCESSORS = (
##    'django.core.context_processors.auth',
##    'django.core.context_processors.debug',
##    'django.core.context_processors.i18n',
##    'django.core.context_processors.media',
##)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["Reading_List_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'books',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cooking.urls'

WSGI_APPLICATION = 'cooking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'books',
        'USER': os.environ['MySQL_USER'],
        'PASSWORD': os.environ['MySQL_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': 'my.cnf'
            }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/


#STATIC_ROOT = BASE_DIR.child('static') 
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR.child('media') 
MEDIA_URL = '/media/'

# EMAIL Settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
