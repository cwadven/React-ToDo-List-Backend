from pathlib import Path
import os
from django.utils import timezone
import datetime
from .env_key import MY_SECRET_KEY
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = MY_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    # DRF
    'rest_framework',
    # 'rest_framework.authtoken',
    # 회원 관련
    'allauth',
    'allauth.socialaccount',
    'allauth.account',
    'django.contrib.sites',
    'rest_auth.registration',

    # cors 문제 해결
    'corsheaders',
]

PROJECT_APPS = [
    'accounts',
    'Todo',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_APPS

SITE_ID = 1

# DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ],
}

APPEND_SLASH = False

# [DRF] 회원가입 시, 입력 요소 변경
# 유저 모델로 사용하기
AUTH_USER_MODEL = 'accounts.Profile'

# response로 보넬 정보들이 적혀있는 Serializer
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.ProfileSerializer',
}

# 회원가입용 SERIALIZER
REST_AUTH_REGISTER_SERIALIZERS = {'REGISTER_SERIALIZER': 'accounts.serializers.ProfileSerializer', }

# 마지막으로 회원가입용 SERIALIZER를 적용시켜주기 위한 단계
ACCOUNT_ADAPTER = 'accounts.adapter.CustomAccountAdapter'

# # 이메일 인증 관련 (메일 보내기!! 인증)
# # 메일을 호스트하는 서버
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'

# # gmail 통신하는 포트
# EMAIL_PORT = '587'

# # 발신할 이메일
# EMAIL_HOST_USER = '구글이메일@gmail.com'
# # 발신할 메일의 비밀번호
# EMAIL_HOST_PASSWORD = '추가적인비밀번호구하기'

# # TLS 보안 방법
# EMAIL_USE_TLS = True

# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# URL_FRONT = 'http://dalgona.me/'
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# # 이메일 필수 일 경우
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# # 이메일 필수 아님
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"

# # 사이트와 관련한 자동응답을 받을 이메일 주소,'webmaster@localhost'
# EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 5
# ACCOUNT_EMAIL_SUBJECT_PREFIX = "이메일 제목"

# JWT 사용
REST_USE_JWT = True

JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATICFILES_DIRS = [
    # 실제 static 파일은 모두 client 측에서 소유 
    os.path.join(BASE_DIR, 'temp_static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

# Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True
