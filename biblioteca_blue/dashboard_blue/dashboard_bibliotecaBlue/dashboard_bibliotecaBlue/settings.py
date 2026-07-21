
from pathlib import Path
 
BASE_DIR = Path(__file__).resolve().parent.parent
 
SECRET_KEY = 'django-insecure-dashboard-biblioteca-blue'
 
DEBUG = True
 
ALLOWED_HOSTS = ['*']
 
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'graficos',
]
 
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]
 
ROOT_URLCONF = 'dashboard_bibliotecaBlue.urls'
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]
 
WSGI_APPLICATION = 'dashboard_bibliotecaBlue.wsgi.application'
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
 
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True
 
STATIC_URL = 'static/'
 
# ── Configuración propia: URLs de los otros microservicios ──────────
WEBAPP_URL = 'http://localhost:8000'   # bibliotecaBlue (préstamos, MongoDB)
WEBSERVICE_URL = 'http://localhost:8001'  # ws_LibrosBlue (catálogo, PostgreSQL)
