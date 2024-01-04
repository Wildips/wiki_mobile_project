import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    selenoid_user: str = os.getenv("LOGIN")
    selenoid_user_password: str = os.getenv("PASSWORD")
    login_mobile: str = os.getenv("LOGIN_MOBILE")
    password_mobile: str = os.getenv("PASSWORD_MOBILE")
    remote_mobile_url: str = os.getenv("REMOTE_MOBILE_URL")
    local_mobile_url: str = os.getenv("LOCAL_MOBILE_URL")
    app_wait_activity: str = os.getenv("APP_WAIT_ACTIVITY")
    browserstack_app: str = os.getenv("BROWSERSTACK_APP")
    local_emulator_app: str = os.getenv("LOCAL_EMULATOR_APP")
    #######
    # remote, local_real, local_emulator
    context: str = os.getenv("CONTEXT")


settings = Settings()
