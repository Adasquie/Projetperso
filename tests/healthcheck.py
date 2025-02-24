from flask import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('healthcheck', __name__)

@bp.route('/health')
def health_check():
    """Basic health check endpoint."""
    logger.info("Health check endpoint called")
    try:
        return jsonify({
            'status': 'healthy',
            'message': 'Application is running'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500 