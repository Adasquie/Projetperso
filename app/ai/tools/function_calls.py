import json
import requests
import logging
from app.core.auth_handler import AuthHandler
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
auth_handler = AuthHandler()

logger = logging.getLogger(__name__)

def send_email(tool):
    """Répond à un email en récupérant le message_id du dernier email reçu"""
    
    arguments = json.loads(tool.function.arguments)
    to = arguments.get("to", "inconnu")
    subject = arguments.get("subject", "Aucun sujet")
    body = arguments.get("body", "Pas de contenu")

    # 🔍 Récupérer le dernier message_id via Microsoft Graph
    message_id = get_latest_email_id()

    if not message_id:
        logger.error("❌ Impossible de récupérer le message_id.")
        return {"tool_call_id": tool.id, "output": "Erreur: message_id introuvable."}

    logger.info(f"📩 Réponse à {to} | Sujet: {subject} | Contenu: {body} | Message ID: {message_id}")

    try:
        token = auth_handler.get_app_token()
        user_id = "alexandredasquie@alexandredasquie.onmicrosoft.com"
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}/reply"

        payload = {
            "comment": body,  # La réponse
            "message": {
                "toRecipients": [{"emailAddress": {"address": to}}],
                "subject": subject
            }
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 202:
            logger.info(f"✅ Email envoyé avec succès à {to}")
            return {"tool_call_id": tool.id, "output": "Email envoyé avec succès ✅"}
        else:
            logger.error(f"❌ Erreur envoi email à {to}: {response.status_code} - {response.text}")
            return {"tool_call_id": tool.id, "output": f"Échec de l'envoi: {response.text}"}

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'envoi de l'email: {e}")
        return {"tool_call_id": tool.id, "output": "Erreur lors de l'envoi de l'email ❌"}
    
def get_latest_email_id():
    """Récupère le message_id du dernier email non lu"""
    try:
        token = auth_handler.get_app_token()
        user_id = "alexandredasquie@alexandredasquie.onmicrosoft.com"
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages?$filter=isRead eq false&$orderby=receivedDateTime desc&$top=1"

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            messages = response.json().get("value", [])
            if messages:
                return messages[0]["id"]  # Retourne le message_id du dernier email reçu
            else:
                logger.warning("⚠️ Aucun email non lu trouvé.")
                return None
        else:
            logger.error(f"❌ Erreur API Graph: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération du message_id: {e}")
        return None