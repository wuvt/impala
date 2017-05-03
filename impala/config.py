import os

class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = "changeme"
    SQLALCHEMY_DATABASE_URI = "postgresql://impala:4DhEJW3gFyPtEF4DmZmChJ@localhost/impala"

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
