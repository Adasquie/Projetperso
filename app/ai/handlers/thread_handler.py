from openai import OpenAI
import logging
from typing import List
import re
from typing import Optional

logger = logging.getLogger(__name__)

class ThreadHandler:
    def __init__(self, client: OpenAI, assistant_id: str):
        self.client = client
        self.assistant_id = assistant_id

    def add_message_to_thread(self, thread_id: str, message: str):
        """Ajoute un message utilisateur à un thread existant."""
        try:
            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'ajout du message au thread {thread_id}: {e}")

    def get_thread_messages(self, thread_id: str) -> List[str]:
        """Récupère tous les messages d'un thread."""
        try:
            response = self.client.beta.threads.messages.list(thread_id=thread_id)
            return [msg.content[0].text.value for msg in response.data if msg.role in ["user", "assistant"]]
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des messages du thread {thread_id}: {e}")
            return []


    def create_thread(self, email_content: str) -> str:
        """Crée un nouveau thread et y ajoute l'email reçu."""
        response = self.client.beta.threads.create()
        new_thread_id = response.id
        self.add_message_to_thread(new_thread_id, email_content)
        return new_thread_id
    
    def find_existing_thread(self, email_content: str) -> Optional[str]:
        """Recherche un thread existant en interrogeant l'Assistant OpenAI avec accès à la base vectorielle."""
        try:
            response = self.client.beta.threads.create()
            thread_id = response.id

            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=f"Peux-tu retrouver un thread correspondant à cet email ? {email_content}\nSi oui, donne-moi le thread_id."
            )

            run_status = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=self.assistant_id
            )

            if run_status.status == "completed":
                messages = self.get_thread_messages(thread_id)
                for msg in messages:
                    match = re.search(r"thread_id: (\S+)", msg)
                    if match:
                        return match.group(1)
        except Exception as e:
            logger.error(f"❌ Erreur lors de la recherche du thread existant : {e}")
        return None
    
    def get_last_response(self, thread_id: str) -> Optional[str]:
        """Récupère la dernière réponse de l'IA pour un thread donné."""
        try:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            for msg in reversed(messages.data):  # On commence par le plus récent
                if msg.role == "assistant":
                    return msg.content[0].text.value.strip()
        except Exception as e:
            logger.error(f"❌ Erreur récupération réponse IA pour thread {thread_id}: {e}")
        return None