import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://dennis:dennis@localhost/fashionyuva"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "46ergsgwet5w5fewfweffhdgh")
