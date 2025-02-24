class TokenExpiredError(Exception):
    """Levée quand le token d'accès est expiré"""
    pass

class AuthenticationError(Exception):
    """Levée pour les erreurs d'authentification"""
    pass

class EmailProcessingError(Exception):
    """Levée pour les erreurs de traitement des emails"""
    pass 