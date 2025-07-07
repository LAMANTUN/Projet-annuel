import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carto_project.settings')
django.setup()

from carto_app.models import Serveur, Application

# Nettoyage
Serveur.objects.all().delete()
Application.objects.all().delete()

# Création des serveurs
serveur_web1 = Serveur.objects.create(nom='Serveur Web 1')
serveur_web2 = Serveur.objects.create(nom='Serveur Web 2')
serveur_db1 = Serveur.objects.create(nom='Serveur DB 1')
serveur_api = Serveur.objects.create(nom='Serveur API')
serveur_backup = Serveur.objects.create(nom='Serveur Backup')

# Applications avec installation sur plusieurs serveurs
apps_data = [
    ('Python', '3.11', [serveur_web1, serveur_web2, serveur_api]),
    ('PostgreSQL', '15', [serveur_db1, serveur_backup]),
    ('Nginx', '1.23', [serveur_web1, serveur_web2]),
    ('Node.js', '18', [serveur_web2, serveur_api]),
    ('Docker', '24.0', [serveur_api]),
    ('Redis', '7.0', [serveur_db1, serveur_api]),
    ('MongoDB', '6.0', [serveur_backup]),
]

for app_name, version, serveurs in apps_data:
    for srv in serveurs:
        Application.objects.create(nom=app_name, version=version, serveur=srv)

print("✅ Serveurs et applications insérés avec succès.")
