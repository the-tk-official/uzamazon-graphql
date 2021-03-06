"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#i($ge=16+naj#-5&7macjf1rjaj82ub_z40t951&dh@dk42je'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Required for GraphiQL
    'graphene_django',

    # Refresh tokens are optional
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',

    # GraphQL authentication
    'graphql_auth',

    # Django-filters
    'django_filters',

    # Local apps
    'user.apps.UserConfig',
    'product.apps.ProductConfig',
]

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'backend/static'
]
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GRAPHENE = {
    'SCHEMA': 'backend.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
        'backend.middlewares.CustomPaginationMiddleware'
    ],
}

AUTHENTICATION_BACKENDS = [
    # remove this
    # 'graphql_jwt.backends.JSONWebTokenBackend',

    # add this
    'graphql_auth.backends.GraphQLAuthBackend',

    'django.contrib.auth.backends.ModelBackend'
]

GRAPHQL_JWT = {
    'JWT_ALLOW_ANY_CLASSES': [
        'graphql_auth.mutations.Register',
        'graphql_auth.mutations.VerifyAccount',
        'graphql_auth.mutations.ResendActivationEmail',
        'graphql_auth.mutations.SendPasswordResetEmail',
        'graphql_auth.mutations.PasswordReset',
        'graphql_auth.mutations.ObtainJSONWebToken',
        'graphql_auth.mutations.VerifyToken',
        'graphql_auth.mutations.RefreshToken',
        'graphql_auth.mutations.RevokeToken',
        'graphql_auth.mutations.VerifySecondaryEmail',
    ],

    'JWT_VERIFY_EXPIRATION': True,

    # optional
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
}

GRAPHQL_AUTH = {
    'ALLOW_LOGIN_NOT_VERIFIED': False,
    # Use email field for login
    'LOGIN_ALLOWED_FIELDS': {'email': 'String', },
    # Fields for register mutation
    'REGISTER_MUTATION_FIELDS': {
        'email': 'String',
        'first_name': 'String',
        'last_name': 'String',
        'dob': 'String',
        'phone_number': 'String',
        'gender': 'String'
    },
    'UPDATE_MUTATION_FIELDS': {
        'email': 'String',
        'first_name': 'String',
        'last_name': 'String',
        'dob': 'String',
        'phone_number': 'String',
        'gender': 'String',
        'is_active': 'Boolean',
        'is_staff': 'Boolean',
        'is_superuser': 'Boolean'
    },
    # User authentication by a specific field
    'USERNAME_FIELD': {
        'email': 'String',
    },
    # Tell 'django-filter' which fields to filter
    'USER_NODE_FILTER_FIELDS': {
        'email': ['icontains', ],
        'is_active': ['exact', ],
        'is_staff': ['exact', ],
        'is_superuser': ['exact', ],
        'status__archived': ['exact', ],
        'status__verified': ['exact', ]
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
