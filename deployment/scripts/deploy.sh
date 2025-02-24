#!/bin/bash

echo "🚀 Déploiement de l'application..."

# Vérifier que nous sommes sur main/master
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
    echo "❌ Erreur: Vous devez être sur la branche main ou master"
    exit 1
fi

# Vérifier que tout est commité
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Erreur: Il y a des changements non commités"
    exit 1
fi

# Générer les certificats si nécessaire
if [ ! -f "certs/cert.pem" ] || [ ! -f "certs/key.pem" ]; then
    echo "🔐 Génération des certificats SSL..."
    ./deployment/scripts/generate_certs.sh
fi

# Construire l'image Docker
echo "🏗️ Construction de l'image Docker..."
docker build -t outlook-assistant .

# Démarrer le conteneur
echo "🚀 Démarrage du conteneur..."
docker run -d \
    --name outlook-assistant \
    -p 8000:8000 \
    --env-file .env \
    -v $(pwd)/certs:/app/certs \
    -v $(pwd)/logs:/app/logs \
    outlook-assistant

echo "✅ Déploiement terminé!"
echo "📝 Logs disponibles avec: docker logs -f outlook-assistant" 