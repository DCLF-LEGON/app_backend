from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tzh5cn7w$l24cpi^)y6un$b&^mzpgu*@u74ns=gsf+rn(e^82n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEPLOYMENT = False


ALLOWED_HOSTS = ['188.166.43.176', '164.90.196.39', '*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',
    'knox',
    "corsheaders",

    # project apps
    'accounts.apps.AccountsConfig',
    'dashboard.apps.DashboardConfig',
    'api.apps.ApiConfig',
    'documentation.apps.DocumentationConfig',

    # REMEMBER ME APP
    # 'auth_remember',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'auth_remember.middleware.AuthRememberMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
if not DEPLOYMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # use postgresql database in production
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'dlcf_db'),
            'USER': os.environ.get('DB_USER', 'dlcfsuperuser'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'AVNS_HO40oOpNF_dSn-nWyRc'),
            'HOST': 'private-dlcfappdb-do-user-12828321-0.b.db.ondigitalocean.com',
            'PORT': '25060',
        },
    }


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

# custom user model
AUTH_USER_MODEL = 'accounts.User'


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles/'

MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = BASE_DIR / 'media/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
# REST_FRAMEWORK = {
#     'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'}

# django cors headers settings
CORS_ALLOW_ALL_ORIGINS = True

# FOR THE IMPLEMENTATION OF REMEMBER ME FUNCTIONALITY
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'auth_remember.backend.AuthRememberBackend',
# )
# AUTH_REMEMBER_COOKIE_NAME = 'remember_token'
# AUTH_REMEMBER_COOKIE_AGE = 86400 * 28  # 4 weeks by default
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# enviroment variables
PAYHUB_SECRET_TOKEN = os.environ.get(
    'PAYHUB_SECRET_TOKEN', "52b9b46af6c82f6eaa9eaaba4dff677378e525e89d73fcaa54c34154e189d4e4")
PAYHUB_WALLET_ID = os.environ.get('PAYHUB_WALLET_ID', "2632e418-05a2-4a49-9eee-5fc22740ac57")  # noqa
ARKESEL_API_KEY = os.environ.get('ARKESEL_API_KEY', 'OkhnOUlLV1FhSlpLQktXN0M=')

# email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'dlcflegonapp@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'jugowqakbtjgvqyw')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
