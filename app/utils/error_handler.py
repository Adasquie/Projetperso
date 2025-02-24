from flask import jsonify, current_app
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    def __init__(self, message, status_code=500, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def setup_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        logger.error(f"API Error: {error.message}")
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Une erreur inattendue s'est produite")
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": "Not Found",
            "message": str(e)
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        if current_app.debug:
            return f"Error: {error}", 500
        return "Internal Server Error", 500 