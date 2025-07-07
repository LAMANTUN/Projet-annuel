#!/bin/sh

echo "⏳ Attente de la base PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Base PostgreSQL accessible. Lancement des migrations..."
python manage.py migrate

echo "👤 Création du superutilisateur si nécessaire..."
python manage.py createsuperuser --noinput || true

echo "🚀 Lancement du serveur Django..."
python manage.py runserver 0.0.0.0:8000
