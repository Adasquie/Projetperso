from functools import wraps
from flask import session, redirect, request, current_app, jsonify
import secrets

def setup_security(app):
    # Configuration de base de la sécurité
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 heure
    
    # Configuration CORS si nécessaire
    # app.config['CORS_HEADERS'] = 'Content-Type'

    @app.before_request
    def force_https():
        if not current_app.debug:  # Utiliser debug au lieu de env
            if request.headers.get('X-Forwarded-Proto', 'http') == 'http':
                url = request.url.replace('http://', 'https://', 1)
                return redirect(url, code=301)

    @app.after_request
    def add_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access_token' not in session:
            return redirect('/auth/login')
        return f(*args, **kwargs)
    return decorated

def handle_auth_error(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': 'Authentication failed',
                'message': str(e)
            }), 401
    return decorated 