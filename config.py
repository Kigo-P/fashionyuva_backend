import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    ## SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@localhost/fashionyuva"
    SQLALCHEMY_DATABASE_URI = f"postgresql://dennis:TTOszQYBlz7ljFPdZhQtlFvd3PucGvwi@dpg-cso8dj8gph6c73bo21vg-a/fashionyuva"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "46ergsgwet5w5fewfweffhdgh")
