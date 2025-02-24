#!/bin/bash

# Variables de la base de données
DB_NAME="outlook_db"
DB_USER="outlook_user"
DB_PASSWORD="votre_mot_de_passe_securise"

# Créer l'utilisateur et la base de données
sudo -u postgres psql << EOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
CREATE DATABASE $DB_NAME OWNER $DB_USER;
\q
EOF

# Mettre à jour le fichier .env.production avec les nouvelles informations
sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME|" .env.production

echo "Base de données configurée avec succès" 