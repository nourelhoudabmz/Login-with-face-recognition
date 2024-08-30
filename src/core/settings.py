import os
from pathlib import Path
from .env import config

# Construction des chemins à l'intérieur du projet comme ceci : BASE_DIR / 'subdir'.
# La ligne suivante est commentée pour utiliser une méthode alternative pour définir BASE_DIR.
# BASE_DIR = Path(__file__).resolve().parent.parent

# Définir BASE_DIR comme le répertoire parent du fichier en cours.
# Il s'agit de la racine du projet Django, utile pour définir des chemins relatifs.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paramètres de développement rapide - inappropriés pour la production.
# Voir la liste de contrôle de déploiement Django pour les paramètres de production appropriés.
# https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# AVERTISSEMENT DE SÉCURITÉ : gardez la clé secrète utilisée en production secrète !
SECRET_KEY = 'django-insecure-84t-z6$bwd-!fc!*$%&+m=0&=gmhqd+w5*x(4!o^tc$w623t(^'

# AVERTISSEMENT DE SÉCURITÉ : ne pas exécuter avec le mode DEBUG activé en production !
DEBUG = True

# Hôtes autorisés pour cette application. Actuellement vide, à configurer pour la production.
ALLOWED_HOSTS = []


# Définition des applications installées dans ce projet Django.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications personnalisées
    'accounts',
]

# Liste des middleware actifs pour traiter les requêtes et les réponses.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Répertoire racine des URL de l'application.
ROOT_URLCONF = 'core.urls'

# Configuration des templates Django.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

# Déclaration de l'application WSGI.
WSGI_APPLICATION = 'core.wsgi.application'


# Configuration de la base de données.
# Actuellement configurée pour utiliser SQLite, idéale pour le développement mais à remplacer pour la production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Validation des mots de passe.
# Les règles suivantes aident à garantir des mots de passe sécurisés.
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


# Modèle utilisateur personnalisé utilisé pour l'authentification.
AUTH_USER_MODEL = 'accounts.NewUser'

# Paramètres de localisation et de langue.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Configuration des fichiers statiques et des fichiers média.
# Les fichiers statiques (CSS, JavaScript, images) sont servis depuis STATIC_URL.
STATIC_URL = 'static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "core/static"),
]

# Les fichiers média (téléchargements des utilisateurs) sont servis depuis MEDIA_URL.
MEDIA_URL = 'media/'
MEDIA_ROOT = 'media'

# Définir le type de champ de clé primaire par défaut.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configuration de l'envoi d'e-mails.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD', default=None)


# Paramètres Celery pour la gestion des tâches asynchrones.
CELERY_BROKER_URL = "redis://localhost:6379"  # URL du courtier de messages Redis.
CELERY_RESULT_BACKEND = "redis://localhost:6379"  # URL du backend des résultats Redis.
CELERY_ACCEPT_CONTENT = ['application/json']  # Formats de contenu acceptés pour les tâches.
CELERY_TASK_SERIALIZER = 'json'  # Sérialiseur pour les tâches.
CELERY_RESULT_SERIALIZER = 'json'  # Sérialiseur pour les résultats des tâches.
CELERY_TIMEZONE = TIME_ZONE  # Fuseau horaire utilisé pour les tâches périodiques.
