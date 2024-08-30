from __future__ import absolute_import, unicode_literals
from celery import shared_task  # Importe le décorateur `shared_task` de Celery pour définir des tâches asynchrones.

from django.core.mail import EmailMessage  # Importe `EmailMessage` pour envoyer des emails.


@shared_task
def send_email(title, email):
    """
    Tâche Celery pour envoyer un email au manager decrit l'emotion de m'utilisateur .
    
    Paramètres :
    - title (str) : Le titre de l'email.
    - email (str) : L'adresse email du destinataire.
    """
    subject = "Hello Our New User, Welcome."  # Sujet de l'email envoyé à l'utilisateur.
    send_email = EmailMessage(title, subject, to=[email])  # Crée un objet `EmailMessage` avec le titre et le sujet.
    send_email.send()  # Envoie l'email à l'adresse spécifiée.

############################################################################
## tâches planifiées

from celery import Celery  # Importe Celery pour définir une application Celery.

app = Celery()  # Crée une instance de l'application Celery.

@app.task(name="add_two_numbers")
def add(x, y):
    """
    Tâche Celery simple pour ajouter deux nombres.
    
    Paramètres :
    - x (int/float) : Premier nombre.
    - y (int/float) : Deuxième nombre.
    
    Retourne :
    - La somme de x et y.
    """
    return x + y  # Retourne la somme des deux nombres.
