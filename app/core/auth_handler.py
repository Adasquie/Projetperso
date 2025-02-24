import time
import msal
from ..config.settings import Config

class AuthHandler:
    def __init__(self):
        self.app = msal.ConfidentialClientApplication(
            client_id=Config.CLIENT_ID,
            client_credential=Config.CLIENT_SECRET,
            authority=f"https://login.microsoftonline.com/{Config.TENANT_ID}"
        )
        self.token = None
        self.token_expiration = 0  # Timestamp d'expiration

    def get_app_token(self):
        """Récupère un token M2M et le stocke temporairement pour éviter les requêtes inutiles."""
        if self.token and time.time() < self.token_expiration:
            return self.token  # Retourne le token encore valide

        result = self.app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" in result:
            self.token = result["access_token"]
            self.token_expiration = time.time() + 3500  # On laisse une marge de 100s avant expiration
            return self.token
        else:
            raise Exception(f"Erreur d'authentification: {result.get('error_description')}")