import logging
import logging.handlers
import os

def setup_logging(app):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Log file handler
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/app.log',
        maxBytes=10000000,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Réduire les logs de httpx
    logging.getLogger("httpx").setLevel(logging.WARNING) 