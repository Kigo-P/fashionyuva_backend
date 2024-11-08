import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "46ergsgwet5w5fewfweffhdgh")
