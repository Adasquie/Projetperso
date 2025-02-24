#!/bin/bash

# Créer le dossier certs s'il n'existe pas
mkdir -p certs

# Générer un certificat auto-signé
openssl req -x509 -newkey rsa:4096 -nodes \
  -out certs/cert.pem \
  -keyout certs/key.pem \
  -days 365 \
  -subj "/C=FR/ST=IDF/L=Paris/O=Dev/CN=localhost"

# Définir les permissions
chmod 600 certs/key.pem
chmod 644 certs/cert.pem

echo "✅ Certificats SSL générés avec succès" 