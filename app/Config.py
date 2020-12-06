from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()


class Config:
    SECRET_KEY = 'mysecretkey'
    DEBUG = False
    ENV = 'production'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(os.getenv('DB_USER'), os.getenv('DB_PASS'),
    #                                                               os.getenv('DB_URL'), str(os.getenv('DB_PORT')),
    #                                                               os.getenv('DB_NAME'))
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
