import logging
import sys
import threading
import time
from app import create_app

import requests

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger()

logging.getLogger("openai").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("msal").setLevel(logging.INFO)

try:
    logger.info("Démarrage de l'application...")
    app = create_app()
    logger.info("Application créée avec succès")
except Exception as e:
    logger.error(f"Erreur lors du démarrage: {e}", exc_info=True)
    raise

def on_startup():
    """Teste le flux M2M en appelant /m2m/emails."""
    time.sleep(5)  # Attendre que l'app soit prête
    base_url = "https://outlook-production.up.railway.app"
    session = requests.Session()

    try:
        # Exemple : user_id = paramètre GET
        user_id = "AlexandreDasquie@AlexandreDasquie.onmicrosoft.com"
        response = session.get(f"{base_url}/m2m/emails?user_id={user_id}")
        if response.status_code == 200:
            logger.info("✅ M2M emails récupérés avec succès")
        else:
            logger.warning(f"⚠️ Échec M2M /m2m/emails: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"❌ Erreur au démarrage (M2M): {e}", exc_info=True)

startup_thread = threading.Thread(target=on_startup, daemon=True)
startup_thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)