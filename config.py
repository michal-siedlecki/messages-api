import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    if 'postgres' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI.replace('postgres', 'postgresql')

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True