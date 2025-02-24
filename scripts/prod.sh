#!/bin/bash

# Vérifier les certificats
if [ ! -f "certs/cert.pem" ] || [ ! -f "certs/key.pem" ]; then
    echo "❌ Certificats SSL manquants. Exécutez ./deployment/scripts/generate_certs.sh"
    exit 1
fi

# Démarrer Gunicorn
export FLASK_ENV=production
gunicorn --config deployment/gunicorn_config.py wsgi:app 