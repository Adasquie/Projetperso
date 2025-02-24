from flask import Blueprint, jsonify
import requests
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from openai import OpenAI
from ..ai.handlers.thread_handler import ThreadHandler
import os
from ..ai.handlers.assistant_handler import EventHandler
from ..core.auth_handler import AuthHandler

bp = Blueprint("m2m", __name__, url_prefix="/m2m")
logger = logging.getLogger(__name__)
thread = "thread_Bz0Kz9sARsjySysdgD9Jtga5"

auth_handler = AuthHandler()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
vector_store_id = "vs_67a9f99ecca881918c93306f20fa9633"
assistant_id = "asst_99mJpGIHpflRxtEOi6CKlrPa"


thread_handler = ThreadHandler(client, assistant_id)

scheduler = BackgroundScheduler()

email_threads = {}  # ⬅ Stocke les threads associés aux emails

import re

def check_emails():
    """Récupère les emails non lus et les envoie à l'IA pour analyse."""
    global last_checked_email_id, last_check_time

    try:
        token = auth_handler.get_app_token()
        user_id = "alexandredasquie@alexandredasquie.onmicrosoft.com"
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages?$filter=isRead eq false"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(graph_url, headers=headers)

        if response.status_code != 200:
            logger.error(f"❌ Erreur API Graph: {response.status_code}")
            return

        messages = response.json().get("value", [])
        if not messages:
            logger.info("📭 Aucun nouvel email non lu.")
            return

        for message in messages:
            email_id = message.get("id")
            sender_email = message.get("from", {}).get("emailAddress", {}).get("address", "")
            subject = message.get("subject", "")
            email_content = message.get("body", {}).get("content", "")
            # Ne pas traiter ses propres emails
            if sender_email.lower() == user_id.lower():
                continue

            # 📝 Ajoute l'email dans un thread OpenAI


            client.beta.threads.messages.create(
                thread_id=thread,
                role="user",
                content=f"""
            Tu dois rédiger une réponse à cet email de manière professionnelle et formelle.

            - Réponds directement au message reçu.
            - Commence ta réponse par une phrase de politesse adaptée.
            - Ne répète pas le message précédent.
            Informations sur l'email :
            - Expéditeur : {sender_email}
            - Sujet : {subject}
            - Contenu :
            ---
            {email_content}
            ---
            Utilise l'outil 'send_email' pour envoyer ta réponse.
            """,
            )

            # 🚀 Démarre le run en streaming
            with client.beta.threads.runs.stream(
                thread_id=thread,
                assistant_id=assistant_id,
                event_handler=EventHandler(client,thread,assistant_id)
            ) as stream:
                stream.until_done()
                mark_email_as_read(user_id, email_id)  # Marque l'email comme lu

    except Exception as e:
        logger.error(f"❌ Erreur dans la lecture des emails: {e}")

def send_auto_reply(user_id, recipient_email, email, response_text):
    """Envoie une réponse automatique basée sur l'analyse de l'IA."""
    try:
        token = auth_handler.get_app_token()
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/sendMail"

        payload = {
            "message": {
                "subject": f"Re: {email.get('subject', 'Votre message')}",
                "body": {"contentType": "Text", "content": response_text},
                "toRecipients": [{"emailAddress": {"address": recipient_email}}]
            },
            "saveToSentItems": "true"
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 202:
            logger.info(f"✅ Email envoyé à {recipient_email}")
        else:
            logger.error(f"❌ Erreur envoi email à {recipient_email}: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email: {e}")

def mark_email_as_read(user_id, email_id):
    """Marque un email comme lu dans Microsoft Graph."""
    try:
        token = auth_handler.get_app_token()
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{email_id}"

        payload = {"isRead": True}
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            logger.info(f"📩 Email {email_id} marqué comme lu.")
        else:
            logger.error(f"❌ Échec de la mise à jour de l'email {email_id}: {response.status_code}")
    except Exception as e:
        logger.error(f"Erreur lors du marquage de l'email comme lu: {e}")

def process_responses():
    """Récupère les réponses de l'IA et envoie les emails."""
    user_id = "alexandredasquie@alexandredasquie.onmicrosoft.com"
    for email_id, data in email_threads.items():
        thread_id = data["thread_id"]
        sender_email = data["sender"]
        email = data["email"]

        response_text = thread_handler.get_last_response(thread_id)

        if response_text:
            send_auto_reply(user_id, sender_email, email, response_text)
            logger.info(f"✅ Réponse envoyée pour l'email {email_id}")
        else:
            logger.warning(f"⚠️ Aucune réponse générée pour le thread {thread_id}")

# Démarrer la tâche périodique
def start_scheduler():
    scheduler.add_job(check_emails, 'interval', minutes=5)
    #scheduler.add_job(process_responses, 'interval', minutes=5)  # ⬅ Ajout du traitement des réponses
    scheduler.start()

start_scheduler()

@bp.route("/emails")
def get_emails_m2m():
    """Lit les emails via un token M2M."""
    try:
        check_emails()
        return jsonify({"status": "success", "message": "Emails analysés"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500