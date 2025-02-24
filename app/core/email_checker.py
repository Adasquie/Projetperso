import threading
import time
from flask import current_app
from .email_handler import EmailHandler
from ..config.settings import Config
from .token_store import token_store

class EmailChecker:
    def __init__(self):
        self.email_handler = EmailHandler(Config.ASSISTANT_ID)
        self.running = False
        self.thread = None

    def start(self, app):
        if self.running:
            return

        def check_loop():
            with app.app_context():
                while self.running:
                    try:
                        token = token_store.get_token()
                        if token:
                            self.email_handler.check_new_emails(token)
                            current_app.logger.info("✓ Vérification périodique des emails effectuée")
                    except Exception as e:
                        current_app.logger.error(f"Erreur lors de la vérification périodique : {e}")
                    time.sleep(60)

        self.running = True
        self.thread = threading.Thread(target=check_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

email_checker = EmailChecker() 