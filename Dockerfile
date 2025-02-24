# 🏗️ Utilisation d'une image légère de Python
FROM python:3.9-slim

# Limiter la mémoire pour Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONMALLOC=malloc
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV PYTHONHASHSEED=random

# 🏠 Définir le dossier de travail dans le conteneur
WORKDIR /app

# 📂 Copier les fichiers du projet
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p logs

# Port dynamique pour Railway
ENV PORT=8000

# 🎬 Commande de lancement
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app