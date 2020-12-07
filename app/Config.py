from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from decouple import config

#load_dotenv()


class Config:
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = 'mysecretkey'
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(config('DB_USER', default='postgres'),
                                                                   config('DB_PASS', default='postgres'),
                                                                   config('DB_URL', default='localhost'),
                                                                   config('DB_PORT', default='5432'),
                                                                   config('DB_NAME', default='users'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)


class ProductionConfig(Config):
    SECRET_KEY = 'MVOBKNcr+abZqgdpZFa19zaVUSKpL9GNBaqTtRnX45U='
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='localhost')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}