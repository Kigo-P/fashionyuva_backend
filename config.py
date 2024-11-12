import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    ENV = os.getenv("ENV", "development")
    if ENV == "production":
        SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URI')
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@localhost/fashionyuva"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "46ergsgwet5w5fewfweffhdgh")
