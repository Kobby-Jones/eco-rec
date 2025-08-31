import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
INSTALLED_APPS = [
"django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
"rest_framework","corsheaders",
"apps.users","apps.catalog","apps.interactions","apps.reco",
]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware","django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates","DIRS": [],"APP_DIRS": True,"OPTIONS": {"context_processors": ["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages",],},},]
WSGI_APPLICATION = None
ASGI_APPLICATION = "config.asgi:application"
DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql","NAME": os.getenv("POSTGRES_DB","app"),"USER": os.getenv("POSTGRES_USER","app"),"PASSWORD": os.getenv("POSTGRES_PASSWORD","app"),"HOST": os.getenv("DB_HOST","localhost"),"PORT": os.getenv("DB_PORT","5432"),}}
STATIC_URL = "/static/"
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS","http://localhost:5173").split(",")
REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/0")
MODEL_DIR = os.getenv("MODEL_DIR", str(BASE_DIR/".."/"models"))
REST_FRAMEWORK = {"DEFAULT_RENDERER_CLASSES":["rest_framework.renderers.JSONRenderer"]}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOW_CREDENTIALS = True

