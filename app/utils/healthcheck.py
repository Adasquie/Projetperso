from flask import Blueprint, jsonify
import psutil
import os

bp = Blueprint('healthcheck', __name__)

@bp.route('/health')
def health_check():
    """Vérifie l'état de l'application."""
    try:
        # Vérification de base
        health_status = {
            'status': 'healthy',
            'version': '1.0.0',
            'environment': os.getenv('FLASK_ENV', 'development'),
            'system': {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent
            }
        }
        
        # Vérification des certificats SSL
        cert_status = {
            'cert_exists': os.path.exists('certs/cert.pem'),
            'key_exists': os.path.exists('certs/key.pem')
        }
        health_status['ssl'] = cert_status
        
        return jsonify(health_status)
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500 