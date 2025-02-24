import requests
from openai import OpenAI
from flask import session
import time
import logging
from ..ai.handlers.assistant_handler import AssistantHandler
from ..config.settings import Config
from .auth_handler import AuthHandler

logger = logging.getLogger(__name__)

class EmailHandler:
    def __init__(self, assistant_id):
        self.assistant_id = assistant_id
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.graph_api_endpoint = "https://graph.microsoft.com/v1.0"
        self.ai_handler = AssistantHandler(assistant_id)
        self.auth_handler = AuthHandler()

    def connect(self):
        """Établit une connexion au service email."""
        try:
            token = self.auth_handler.get_valid_token()
            if not token:
                logger.error("Échec de la récupération d'un token valide.")
                return False
            
            headers = {
                'Authorization': f'Bearer {token["access_token"]}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(f"{self.graph_api_endpoint}/me", headers=headers)
            
            if response.status_code == 200:
                return True
            else:
                logger.error(f"Échec de la connexion, code: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Erreur de connexion: {e}")
            return False

    def check_new_emails(self, access_token):
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.graph_api_endpoint}/me/messages?$filter=isRead eq false",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 401:
                logger.error("Token expiré.")
                raise TokenExpiredError("Token d'accès expiré.")
                
            response.raise_for_status()
            
            emails = response.json().get('value', [])

            if not emails:
                return {"status": "success", "processed": 0}

            for email in emails:
                email_content = email.get("body", {}).get("content", "")

                ai_handler = AssistantHandler(assistant_id=Config.ASSISTANT_ID)
                ai_response = ai_handler.analyze_email(email_content)

                if ai_response and ai_response.action == "répondre":
                    self.send_email(
                        access_token=access_token,
                        subject=f"Re: {email.get('subject', 'Sans sujet')}",
                        content=ai_response.reponse,
                        recipients=[email["from"]["emailAddress"]["address"]]
                    )

            return {"status": "success", "processed": len(emails)}

        except requests.exceptions.Timeout:
            logger.error("Timeout lors de la requête Outlook.")
            return {"error": "Timeout Outlook API"}, 504

        except Exception as e:
            logger.error(f"Erreur lors de la récupération des emails: {e}", exc_info=True)
            return {"error": "Erreur Outlook API"}, 500

    def send_email(self, access_token, subject, content, recipients):
        """Envoie un email via Microsoft Graph API."""
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            email_data = {
                'message': {
                    'subject': subject,
                    'body': {
                        'contentType': 'HTML',
                        'content': content
                    },
                    'toRecipients': [
                        {
                            'emailAddress': {
                                'address': recipient
                            }
                        } for recipient in recipients
                    ]
                },
                'saveToSentItems': True
            }
            
            response = requests.post(
                f"{self.graph_api_endpoint}/me/sendMail",
                headers=headers,
                json=email_data
            )
            
            if response.status_code != 202:
                logger.error(f"Échec de l'envoi de l'email. Code: {response.status_code}")
                logger.error(f"Réponse: {response.text}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email: {e}")
            return False

    def _mark_as_read(self, access_token, email_id):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        update_data = {'isRead': True}
        
        requests.patch(
            f"{self.graph_api_endpoint}/me/messages/{email_id}",
            headers=headers,
            json=update_data
        )