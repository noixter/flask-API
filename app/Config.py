from datetime import datetime, timedelta


class Config:
    SECRET_KEY = 'mysecretkey'
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost:5432/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
