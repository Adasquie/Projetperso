import os
import logging
from flask import Flask, jsonify
from flask_session import Session
import redis


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # Clé secrète pour Flask (sessions, etc.)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "ma-clé-ultra-secrète")

    from .api import m2m, auth
    app.register_blueprint(m2m.bp)
    app.register_blueprint(auth.bp)
    
    # Route de healthcheck
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})

    logger.info("Application créée avec succès")
    return app