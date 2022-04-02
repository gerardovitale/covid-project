from pymongo import MongoClient
from pymongo.database import Database


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(object):
    TESTING = False
    DEBUG = False
    DB_SERVER = None
    DB_NAME = None
    STATIC_FOLDER = None
    TEMPLATE_FOLDER = None

    @property
    def DATABASE_URI(self) -> str:
        return f'mongodb://mongo_db:{self.DB_SERVER}/{self.DB_NAME}'

    @property
    def DATABASE_OBJ(self) -> Database:
        return MongoClient(f'mongodb://mongo_db:{self.DB_SERVER}') \
            .get_database(self.DB_NAME)


class ProductionConfig(Config, metaclass=Singleton):
    pass


class DevelopmentConfig(Config, metaclass=Singleton):
    ENV = 'development'
    DEBUG = True

    HOST = '0.0.0.0'
    PORT = 5001

    STATIC_FOLDER = 'views/static'
    TEMPLATE_FOLDER = 'views/templates'

    DB_SERVER = '27017'
    DB_NAME = 'covid-project'


class TestingConfig(Config, metaclass=Singleton):
    ENV = 'testing'
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False

    DB_SERVER = '27017'
    DB_NAME = 'covid-project'
