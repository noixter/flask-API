from datetime import timedelta

from decouple import config


class Config:
    pass


class TestConfig(Config):
    FLASK_APP = 'app:create_app("test")'
    DEBUG = True
    SECRET_KEY = config('SECRET_KEY', 'mysecretkey')
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db_test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    FLASK_APP = 'app:create_app("development")'
    SECRET_KEY = config('SECRET_KEY', 'mysecretkey')
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGORITHM = 'HS256'


class ProductionConfig(Config):
    FLASK_APP = 'app:create_app("production")'
    SECRET_KEY = config('SECRET_KEY', 'mysecretkey')
    DEBUG = False
    ENV = 'Production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = \
        f'postgresql://{config("DB_USER", default="postgres")}:{config("DB_PASS", default="postgres")}' \
        f'@{config("DB_HOST", default="localhost")}:{config("DB_PORT", default="5432")}' \
        f'/{config("DB_NAME", default="postgres")}'


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
