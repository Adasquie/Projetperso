from flask import Flask, jsonify
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def create_app():
    logger.info("Starting application creation...")
    app = Flask(__name__)
    
    try:
        logger.info("Configuring application...")
        # Configuration
        if os.getenv('FLASK_ENV') == 'production':
            app.config.from_object('app.config.ProductionConfig')
        else:
            app.config.from_object('app.config.DevelopmentConfig')
            
        logger.info("Registering blueprints...")
        # Register blueprints
        from .utils.healthcheck import bp as healthcheck_bp
        app.register_blueprint(healthcheck_bp)
        
        logger.info("Application creation completed successfully")
        return app
        
    except Exception as e:
        logger.error(f"Error creating app: {e}", exc_info=True)
        raise 