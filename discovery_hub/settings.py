from pathlib import Path
import os
import sys
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-insecure-change-me')
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'accounts','pages','tests',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'discovery_hub.urls'
TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[BASE_DIR/'templates'],
    'APP_DIRS':True,
    'OPTIONS':{
        'context_processors':[
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
WSGI_APPLICATION = 'discovery_hub.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME','discovery_db'),
        'USER': os.getenv('DB_USER','disco_app'),
        'PASSWORD': os.getenv('DB_PASSWORD','CSCI340Fall2025Disco'),
        'HOST': os.getenv('DB_HOST','34.16.174.60'),
        'PORT': int(os.getenv('DB_PORT','5432')),
        'CONN_MAX_AGE': 60,
    }
}

# Use in-memory SQLite database for testing to avoid permission issues and for speed.
if 'test' in sys.argv or 'test' == os.environ.get('DJANGO_ENV'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':8}},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# If DEBUG is False, you need to configure STATIC_ROOT for collectstatic
# and ensure your web server (e.g., Nginx) is configured to serve files from STATIC_ROOT.
# For development with DEBUG=True, STATICFILES_DIRS is sufficient.
# STATIC_ROOT = BASE_DIR / 'staticfiles' # Uncomment and configure if DEBUG is False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'screen1'
LOGOUT_REDIRECT_URL = 'login'

# --- EMAIL CONFIGURATION ---
# For development, emails will be printed to the console.
# For production, configure a real email backend (e.g., SMTP).

# Use console backend for development to see emails in the terminal
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For actual email sending (e.g., using Gmail, SendGrid, etc.)
# You MUST configure these settings with your email provider's details.
# For Gmail, you might need to generate an "App Password".
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mailtrap.io') # Example: 'smtp.gmail.com' or 'smtp.mailtrap.io'
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587)) # Example: 587 for TLS, 465 for SSL
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true' # Use TLS
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true' # Use SSL (usually one or the other, not both)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') # Your email address (e.g., 'your_email@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # Your email password or app-specific password

# Site URL and default sender email
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000') # Your site's base URL
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@discoveryhub.com')

# --- END EMAIL CONFIGURATION ---
