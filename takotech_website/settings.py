"""
Django settings for TakoTech Website - Advanced Tech Company Platform
Modular, Scalable, and Production-Ready  os.getenvuration
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# لود فایل .env
load_dotenv() 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY =  os.getenv('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
# DEBUG =  os.getenv('DEBUG', default=True, cast=bool)
DEBUG = os.getenv("DEBUG", "False") == "True"

# ALLOWED_HOSTS =  os.getenv('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver,*.trycloudflare.com,*.cfargotunnel.com' ).split(',')  # تبدیل به لیست

# Application definition - Modular Architecture
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]
# Admin UI overrides
ADMIN_CSS_OVERRIDES = [
    '/static/css/admin-override.css',
]

THIRD_PARTY_APPS = [
    # REST Framework
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_spectacular',
    
    # Authentication & Security
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'guardian',
    
    # Utilities
    'corsheaders',
    'django_extensions',
    'django_jalali',  # Persian date support
    # 'humanize',
    # Real-time & Async
    # 'channels',  # Uncomment when Redis is available
    
    # Search
    # 'django_elasticsearch_dsl',  # Uncomment when Elasticsearch is available
]

# TakoTech Custom Apps - Independent Modules
TAKOTECH_APPS = [
    'settings_app.apps.SettingsAppConfig',
    'users.apps.UsersConfig',
    'services.apps.ServicesConfig', 
    'products.apps.ProductsConfig',
    'computation_engine.apps.ComputationEngineConfig',
    'sales.apps.SalesConfig',
    'tickets.apps.TicketsConfig',
    'security.apps.SecurityConfig',
    'accounts.apps.AccountsConfig',  # Advanced Accounts Management
    'news.apps.NewsConfig',  # News Management System
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + TAKOTECH_APPS

# Middleware  os.getenvuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'takotech_website.urls'

# Template  os.getenvuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings_app.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'takotech_website.wsgi.application'
ASGI_APPLICATION = 'takotech_website.asgi.application'

# Database  os.getenvuration - MySQL (via .env). Fallback values for local dev
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  os.getenv('DATABASE_DEFAULT_NAME', default='takotech'),
        'USER':  os.getenv('DATABASE_DEFAULT_USER', default='root'),
        'PASSWORD':  os.getenv('DATABASE_DEFAULT_PASSWORD', default=''),
        'HOST':  os.getenv('DATABASE_DEFAULT_HOST', default='127.0.0.1'),
        'PORT':  os.getenv('DATABASE_DEFAULT_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    },
    'logs': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  os.getenv('DATABASE_LOGS_NAME', default='tankhah_logs_db'),
        'USER':  os.getenv('DATABASE_LOGS_USER', default='root'),
        'PASSWORD':  os.getenv('DATABASE_LOGS_PASSWORD', default=''),
        'HOST':  os.getenv('DATABASE_LOGS_HOST', default='127.0.0.1'),
        'PORT':  os.getenv('DATABASE_LOGS_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}

# Redis / Cache  os.getenvuration
REDIS_URL =  os.getenv('REDIS_URL', default='redis://localhost:6379/0')
# USE_REDIS_CACHE =  os.getenv('USE_REDIS_CACHE', default=False, cast=bool)
USE_REDIS_CACHE = os.getenv("USE_REDIS_CACHE", "False") == "True"

# Authentication backends (guardian)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Session  os.getenvuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization and Localization
LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported Languages
LANGUAGES = [
    ('fa', 'فارسی'),
    ('en', 'English'),
    ('ar', 'العربية'),
    ('tr', 'Türkçe'),
]

# Default language for new users
DEFAULT_LANGUAGE = 'fa'

# Locale paths for translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Language detection settings
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 365 * 24 * 60 * 60  # 1 year
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = 'Lax'

# Translation settings
MODELTRANSLATION_DEFAULT_LANGUAGE = 'fa'
MODELTRANSLATION_LANGUAGES = ('fa', 'en')
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('fa', 'en'),
    'fa': ('en',),
    'en': ('fa',),
}

# Static files and Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# RCMS Security  os.getenvuration
from cryptography.fernet import Fernet
RCMS_SECRET_KEY_CIPHER = Fernet(Fernet.generate_key())

# REST Framework  os.getenvuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT  os.getenvuration
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# Django Allauth  os.getenvuration
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Fix for custom User model without username field
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'

# Social Authentication
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'github': {
        'SCOPE': ['user:email'],
    }
}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS Settings
# CORS_ALLOWED_ORIGINS =  os.getenv('CORS_ALLOWED_ORIGINS', default='http://localhost:3000', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", 'http://localhost:3000').split(',')

CORS_ALLOW_CREDENTIALS = True


# Celery  os.getenvuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Channels  os.getenvuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        ' os.getenv': {
            'hosts': [REDIS_URL],
        },
    },
}

# Email  os.getenvuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =  os.getenv('EMAIL_HOST', default='smtp.gmail.com')
# EMAIL_PORT =  os.getenv('EMAIL_PORT', default=587, cast=int)
EMAIL_PORT = os.getenv("EMAIL_PORT", '587')


EMAIL_USE_TLS = True
EMAIL_HOST_USER =  os.getenv('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD =  os.getenv('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL =  os.getenv('DEFAULT_FROM_EMAIL', default='noreply@takotech.com')

# Elasticsearch  os.getenvuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts':  os.getenv('ELASTICSEARCH_HOST', default='localhost:9200')
    },
}

# Logging  os.getenvuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'takotech': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'TakoTech API',
    'DESCRIPTION': 'Advanced Tech Company Platform API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Custom Settings for TakoTech Features
TAKOTECH_SETTINGS = {
    'COMPANY_NAME': 'TakoTech',
    'ENABLE_AI_FEATURES':  os.getenv('ENABLE_AI_FEATURES', 'True').lower() == 'true',
    'ENABLE_SANDBOX':  os.getenv('ENABLE_SANDBOX', 'True').lower() == 'true',
    'MAX_CONCURRENT_COMPUTATIONS':  int(os.getenv('MAX_CONCURRENT_COMPUTATIONS', '10')),
    'DEMO_SESSION_TIMEOUT': 1800,  # 30 minutes
}
