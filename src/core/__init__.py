from .celery import app as celery_app  # Importe l'application Celery définie dans le fichier `celery.py` de votre projet.

__all__ = ('celery_app', )  # Déclare explicitement ce qui est exporté lorsqu'on utilise `from <module> import *`.
