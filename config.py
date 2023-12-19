import os

from dotenv import load_dotenv

load_dotenv()

SELENOID_USER = os.getenv("LOGIN")
SELENOID_USER_PASSWORD = os.getenv("PASSWORD")
LOGIN_MOBILE = os.getenv("LOGIN_MOBILE")
PASSWORD_MOBILE = os.getenv("PASSWORD_MOBILE")
REMOTE_MOBILE_URL = os.getenv("REMOTE_MOBILE_URL")
