from datetime import timedelta
from decouple import config


class Config:
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = config('SECRET_KEY', 'mysecretkey')
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    JWT_ALGORITHM = 'HS256'


class ProductionConfig(Config):
    SECRET_KEY = config('SECRET_KEY', 'mysecretkey')
    DEBUG = False
    ENV = 'Production'
    SQLALCHEMY_DATABASE_URI = \
        f'postgresql://{config("DB_USER", default="postgres")}:{config("DB_PASS", default="postgres")}' \
        f'@{config("DB_URL", default="localhost")}:{config("DB_PORT", default="5432")}' \
        f'/{config("DB_NAME", default="postgres")}'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
