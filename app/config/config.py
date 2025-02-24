from .settings import Config

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    TEMPLATES_AUTO_RELOAD = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True 