#!/bin/bash

# Générer les certificats si nécessaire
if [ ! -f "certs/cert.pem" ] || [ ! -f "certs/key.pem" ]; then
    echo "🔐 Génération des certificats SSL..."
    ./deployment/scripts/generate_certs.sh
fi

# Démarrer l'application en mode développement
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export FLASK_DEBUG=1

python -m flask run --host=0.0.0.0 --port=8000 --cert=certs/cert.pem --key=certs/key.pem 