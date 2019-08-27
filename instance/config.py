# instance/config.py
import os
import sys
class Config():
    DEBUG=False
    SECRET_KEY=os.getenv("JWT_SECRET_KEY") 
    SQLALCHEMY_DATABASE_URI = os.getenv("DATA_BASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Enable our debug mode to True in development in order to auto restart our server on code changes"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DOCKER_DATABASE_URL")

    
class TestingConfig(Config):
    """Testing app configurations"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://test-user@localhost:5432/test-db'
    # SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")

    
class ReleaseConfig(Config):
    """Releasing app configurations"""
    DEBUG = False
    TESTING = False


app_configuration={
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'release': ReleaseConfig,
}

AppConfig = 'testing' if 'pytest' in sys.modules else app_configuration.get(os.getenv('FLASK_ENV'),'development')