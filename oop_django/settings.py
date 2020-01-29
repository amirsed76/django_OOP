import os
import environ


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
env = environ.Env(
    SECRET_KEY=str,
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['127.0.0.1:8000']),
    # ALLOWED_HOSTS=list,
    DATABASE_URL=str,
    AUTH_PASSWORD_VALIDATORS=list,
    CORS_ORIGIN_ALLOW_ALL=bool,
)
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

# ALLOWED_HOSTS=env("ALLOWED_HOSTS")
# ALLOWED_HOSTS=["*"]


INSTALLED_APPS = [
    'add',
    'store',
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'rest_auth.registration',
    'django.contrib.sites',
    'allauth.account',
    'rest_framework_swagger',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oop_django.urls'

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

CORS_ORIGIN_WHITELIST=["https://example.com","https://sub.example.com","http://localhost:8080","http://localhost:4200"]
WSGI_APPLICATION = 'oop_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {

    'default': env.db(),

}
print(DATABASES)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'oop_project',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = env("AUTH_PASSWORD_VALIDATORS")
SITE_ID = 1

# CORS
CORS_ORIGIN_ALLOW_ALL = env('CORS_ORIGIN_ALLOW_ALL')

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = env('STATIC_ROOT')
STATIC_URL = env('STATIC_URL')

AUTH_USER_MODEL = 'store.Customer'

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "store.serializers.CustomUserDetailsSerializer",
}
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "store.serializers.CustomRegisterSerializer",
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination'
}

OLD_PASSWORD_FIELD_ENABLED = True
