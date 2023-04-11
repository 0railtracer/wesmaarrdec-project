"""
Django settings for cmsweb project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w0d@ke1%w(c73d)k@w7tg)nti3z@9=6jys#_95#w3tv0i5d9gf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tiny.db.elephantsql.com', 'wesmaarrdec-test.onrender.com', 'localhost', '127.0.0.1' ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'auth_user',
    'cmsblg',
    'cmscore',
    # 'Chat'
]
AUTH_USER_MODEL = 'auth_user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cmsweb.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'cmsweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        
        # postgres
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'testtetete',
        # 'USER': 'postgres',
        # 'PASSWORD': 'Spaceback24',
        # 'HOST': 'localhost',
        # 'PORT': '5433',

        # postgreslive
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qvmaadup',
        'USER': 'qvmaadup',
        'PASSWORD': '9M0j5yPa9j1Hm4nyzb-vj5slJWVYYO8W',
        'HOST': 'tiny.db.elephantsql.com',
        'PORT': '5432',

        #mysql localhost
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'test101',
        # 'USER': 'root',
        # 'PASSWORD': '',
        # 'HOST': 'localhost',
        # 'PORT': '3306'

        # mysql live
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'epiz_33766009_wesmaarrdec',
        # 'USER': 'epiz_33766009',
        # 'PASSWORD': '88tn1wEA7NsHph5',
        # 'HOST': 'sql204.epizy.com',
        # 'PORT': '3306'
        
    }
}
# AUTH_USER_MODEL = 'auth_user.User'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'twonomber5@gmail.com'
EMAIL_HOST_PASSWORD = 'Spaceback24'

DEFAULT_FROM_EMAIL = 'Your Company <noreply@yourcompany.com>'

EMAIL_SUBJECT_PREFIX = '[Your Company] '
