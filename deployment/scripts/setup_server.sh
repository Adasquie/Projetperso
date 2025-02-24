#!/bin/bash

# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances système
sudo apt install -y python3-pip python3-venv postgresql nginx certbot python3-certbot-nginx

# Création de l'utilisateur système
sudo useradd -m -r -s /bin/bash outlook

# Configuration des permissions
sudo mkdir -p /var/www/outlook
sudo chown -R outlook:outlook /var/www/outlook

# Installation du certificat SSL
sudo certbot --nginx -d votre-domaine.com --non-interactive --agree-tos -m votre@email.com

echo "Configuration serveur terminée" 