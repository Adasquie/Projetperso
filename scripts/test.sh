#!/bin/bash

echo "🔍 Vérification de l'environnement..."

# Vérifier Python
python3 --version || { echo "❌ Python non trouvé"; exit 1; }

# Vérifier les dépendances
pip install -r requirements.txt || { echo "❌ Erreur d'installation des dépendances"; exit 1; }

# Vérifier la configuration
if [ ! -f ".env" ]; then
    echo "❌ Fichier .env manquant"
    exit 1
fi

echo "✅ Environnement OK"

# Démarrer l'application en mode test
echo "🚀 Démarrage de l'application..."
FLASK_ENV=development FLASK_DEBUG=1 python3 wsgi.py 