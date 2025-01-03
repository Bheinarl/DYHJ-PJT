from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*ob(&%ryzc5&*bpb+m8((cv2a#i@+%b!r@wm+c4p@=h)*350vp'

# 환율 API 키 설정
EXCHANGE_RATE_API_KEY = 'TUwyZMxyTt6XP6rTujYY02UCuSPWDHDb'
# 현주 API 키 = "TUwyZMxyTt6XP6rTujYY02UCuSPWDHDb"
# 동연 API 키 = "etB20sfgNjlqWRXSwrActTWgwVjJnsWy"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['dyhj2024.site', '54.89.24.244']

# 사용자 수정
AUTH_USER_MODEL = 'accounts.CustomUser'

CORS_ALLOW_ALL_ORIGINS = True  # 모든 도메인에서 요청 허용 (보안 고려 필요)
# Application definition

INSTALLED_APPS = [

    # APP
    'articles',
    'accounts',
    'stocks',
    'finances',
    'maps',

    # Django contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
]

# 기본 설정 (필요 시 수정)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
}

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pjt.urls'

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

WSGI_APPLICATION = 'pjt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,  # 타임아웃을 20초로 설정
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# static 폴더 설정
import os

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # BASE_DIR에 따라 경로가 적절히 변경될 수 있음

# media 파일 설정 (업로드된 파일 저장)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite 개발 서버 주소 # Vue.js 개발 서버 URL
    'http://127.0.0.1:8000',  # Django 개발 서버 주소
    'http://127.0.0.1:5173',  # Django 개발 서버 주소
    'http://54.89.24.244',    # 서버 배포 서버 주소
    'https://dyhj2024.site',  # 도메인 주소
]

CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_CREDENTIALS = True 설정을 추가하여, 자격 증명(쿠키 또는 인증 정보)도 포함하도록 설정할 수 있습니다.

CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-csrftoken',
    'Access-Control-Allow-Credentials',  # 추가된 헤더
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1:5173',  # Vue.js dev server 주소
    'http://localhost:5173',
    'https://dyhj2024.site',  # 도메인 주소
]

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),  # Authorization 헤더 타입 설정
}

#####################################

# 이메일 인증을 비활성화하고 싶다면 다음 설정을 추가
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = False
LOGIN_URL = '/api/auth/login/'