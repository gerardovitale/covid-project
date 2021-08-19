from pymongo import MongoClient


class Config(object):
    """Base config, uses staging database server."""
    TESTING = False
    DEBUG = False
    DB_SERVER = None
    DB_NAME = None
    STATIC_FOLDER = None
    TEMPLATE_FOLDER = None

    @property
    def DATABASE_URI(self):
        return f'mongodb://mongo_db:{self.DB_SERVER}/{self.DB_NAME}'

    @property
    def DATABASE_OBJ(self):
        return MongoClient(f'mongodb://mongo_db:{self.DB_SERVER}')\
                .get_database(self.DB_NAME)


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

    HOST = '0.0.0.0'
    PORT = 5000

    STATIC_FOLDER = 'views/static'
    TEMPLATE_FOLDER = 'views/templates'

    DB_SERVER = '27017'
    DB_NAME = 'covid-project'


class TestingConfig(Config):
    pass
