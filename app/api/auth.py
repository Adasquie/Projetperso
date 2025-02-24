from flask import Blueprint, jsonify
from ..core.auth_handler import AuthHandler
import logging

bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_handler = AuthHandler()
logger = logging.getLogger(__name__)


@bp.route('/client_credentials')
def client_credentials():
    """
    Exemple de route pour récupérer un token d'app
    via Client Credentials Flow.
    """
    try:
        token = auth_handler.get_app_token()
        logger.debug(f"🔑 Token M2M récupéré: {token[:20]}...")  # Log partiel pour la démo
        # Ici, tu peux appeler une API (Microsoft Graph ou autre) directement
        return jsonify({"access_token": token})
    except Exception as e:
        logger.error(f"Erreur Client Credentials: {e}")
        return jsonify({"error": str(e)}), 500