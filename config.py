import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    ENV = os.getenv("ENV", "development")
    if ENV == "production":
        SQLALCHEMY_DATABASE_URI = f"postgresql://dennis:TTOszQYBlz7ljFPdZhQtlFvd3PucGvwi@dpg-cso8dj8gph6c73bo21vg-a/fashionyuva"
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@localhost/fashionyuva"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "46ergsgwet5w5fewfweffhdgh")

#   for mpesa

    MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
    MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
    MPESA_BUSINESS_SHORTCODE = os.getenv('MPESA_BUSINESS_SHORTCODE')
    MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
    MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')

