from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Configure l'application Celery avec les paramètres de Django.
# Définit le module de paramètres par défaut pour Celery à 'core.settings'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Crée une instance de Celery avec le nom 'core'. Ce nom est utilisé pour identifier l'application Celery.
app = Celery('core')

# Configure Celery pour utiliser les paramètres définis dans les paramètres Django.
# En utilisant une chaîne ici, le travailleur n'a pas besoin de sérialiser l'objet de configuration dans les processus enfants.
# Le namespace 'CELERY' signifie que toutes les clés de configuration liées à Celery doivent avoir le préfixe 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charge les modules de tâches depuis toutes les applications Django enregistrées.
app.autodiscover_tasks()

# Commandes pour exécuter Celery avec des options de journalisation et de pool :
# Pour démarrer un ouvrier Celery : `celery -A core worker -l info`
# Pour démarrer un ouvrier Celery avec le pool 'gevent' : `celery -A core worker -l info -P gevent`

##############################

# Importation de crontab pour la planification des tâches périodiques.
from celery.schedules import crontab 

"""
    - Consultez la documentation sur les tâches périodiques : 
      https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html?highlight=periodic#crontab-schedules
    - Pour démarrer le service de planification Celery Beat : `celery -A core beat -l info`
"""

# Configuration du calendrier des tâches périodiques avec Celery Beat.
app.conf.beat_schedule = {
    # Tâche planifiée pour s'exécuter toutes les minutes, appelant la tâche 'add_two_numbers' avec les arguments (2, 3).
    'add-every-min':{
        'task':'add_two_numbers',
        'schedule': crontab(),
        'args': (2, 3),
    },
    # Tâche planifiée pour s'exécuter toutes les 5 secondes, appelant la tâche 'add_two_numbers' avec les arguments (2, 60).
    'add-every-5-sic':{
        'task':'add_two_numbers',
        'schedule': 5.0,
        'args': (2, 60),
    },
    # Tâche planifiée pour s'exécuter toutes les 30 secondes, appelant la tâche 'add_two_numbers' avec les arguments (2, 60).
    'add-every-30-sic':{
        'task':'add_two_numbers',
        'schedule': 30.0,
        'args': (2, 60),
    }
}
