import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    PROJECT = 'pdx_ulti'

    # Get app root path
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = True

    SECRET_KEY = 'this_is_so_secret' #used for development, reset in prod

    # Flask Security Config
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True

    SECURITY_PASSWORD_HASH = 'bcrypt'

    PRODUCTION = False

class ProductionConfig(Config):

    PRODUCTION = True

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

    DEBUG = False

    #MongoDB Info
    MONGODB_DB = os.environ.get('MONGODB_DATABASE')
    MONGODB_HOST = os.environ.get('MONGO_URL')
    MONGODB_PORT = os.environ.get('MONGODB_PORT')
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')

class DevelopmentConfig(Config):

    # MongoDB Config
    MONGODB_DB = 'pdxulti_db'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    SECURITY_PASSWORD_SALT = '/2aX16zPnnIgfMwkOjGX4S'


class TestingConfig(Config):

    TESTING = True
