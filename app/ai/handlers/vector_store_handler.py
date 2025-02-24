from openai import OpenAI
import logging
from typing import List, Optional
import io
import tempfile

logger = logging.getLogger(__name__)

class VectorStoreHandler:
    def __init__(self, client: OpenAI, vector_store_id: str):
        self.client = client
        self.vector_store_id = vector_store_id

    def format_document(self, thread_id: str, messages: List[str]) -> str:
        """Construit le document avec entête (ThreadID uniquement)."""
        header = f"ThreadID: {thread_id}\n---\n"
        content = "\n".join(messages)
        return header + content

    def store_thread(self, thread_id: str, messages: List[str]):
        """Ajoute ou met à jour un thread dans le Vector Store."""
        document_content = "\n".join(messages)  # Concatène les messages

        # 🔹 1️⃣ Création d'un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(document_content.encode("utf-8"))
            temp_file_path = temp_file.name  # 🔥 On récupère le chemin du fichier

        # 🔹 2️⃣ Upload du fichier en tant que fichier OpenAI
        file_response = self.client.files.create(
            file=open(temp_file_path, "rb"),  # Ouvre le fichier temporaire
            purpose="assistants"
        )
        file_id = file_response.id  # ✅ Récupère l'ID du fichier

        logger.info(f"📂 Fichier uploadé avec succès : {file_id}")

        # 🔹 3️⃣ Suppression de l'ancien thread (si existant)
        self.delete_thread(thread_id)

        # 🔹 4️⃣ Ajout du fichier au Vector Store
        self.client.beta.vector_stores.files.create(
            vector_store_id=self.vector_store_id,
            file_id=file_id  # ✅ Envoie l'ID du fichier
        )

        logger.info(f"✅ Thread {thread_id} stocké dans le Vector Store.")

    def delete_thread(self, thread_id: str):
        """Supprime un thread du Vector Store."""
        documents = self.client.beta.vector_stores.files.list(vector_store_id=self.vector_store_id)

        for doc in documents.data:
            content = self.client.beta.vector_stores.files.retrieve(
                vector_store_id=self.vector_store_id,
                file_id=doc.id
            )
            if f"ThreadID: {thread_id}" in content:
                self.client.beta.vector_stores.files.delete(
                    vector_store_id=self.vector_store_id,
                    file_id=doc.id
                )
                logger.info(f"🗑️ Thread {thread_id} supprimé.")
                return

        logger.warning(f"❌ Aucun document trouvé pour le thread {thread_id}")

