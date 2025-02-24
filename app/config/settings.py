import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class Config:
    # Sécurité
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    
    # OAuth2.0
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    
    # Base de données
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./outlook.db')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ASSISTANT_ID = "asst_99mJpGIHpflRxtEOi6CKlrPa"

    # Scopes OAuth
    SCOPES = ['User.Read', 'Mail.ReadWrite', 'Mail.Send', 'offline_access']

    # Graph API
    GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

    @classmethod
    def get_oauth_config(cls):
        return {
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET,
            'tenant_id': cls.TENANT_ID,
            'redirect_uri': cls.REDIRECT_URI,
            'authority': cls.AUTHORITY,
            'scopes': cls.SCOPES
        }

# Assurez-vous que ces scopes sont corrects et suffisants
REQUIRED_SCOPES = [
    'Mail.Read',
    'Mail.Send',
    'offline_access'
]

OAUTH_SETTINGS = {
    'authority': f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}",
    'client_id': os.getenv('CLIENT_ID'),
    'scope': [
        "https://graph.microsoft.com/Mail.ReadWrite",
        "https://graph.microsoft.com/Mail.Send",
        "https://graph.microsoft.com/User.Read",
        "offline_access"
    ],
    'redirect_uri': os.getenv('REDIRECT_URI')
}

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Autres configurations spécifiques à la production 