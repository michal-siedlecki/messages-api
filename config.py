import os

# ::::::::::::::::::::::::::::::::::::::::::::::

TOKEN = 'token'
API_URL = 'api'
MAX_CONTENT = 160

# ::::::::::::::::::::::::::::::::::::::::::::::

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///messages_testing"

