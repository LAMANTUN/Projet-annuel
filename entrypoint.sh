#!/bin/sh

echo "⏳ Attente de la base PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Base PostgreSQL accessible. Lancement des migrations..."
python manage.py makemigrations
python manage.py migrate

echo "📦 Chargement des données de test (si non chargées)..."
python manage.py loaddata test_data_fixture.json || echo "⚠️  Données déjà chargées ou fichier manquant"

echo "👤 Création du superutilisateur si nécessaire..."
python manage.py createsuperuser --noinput || true

echo "🚀 Lancement du serveur Django..."
python manage.py runserver 0.0.0.0:8000
