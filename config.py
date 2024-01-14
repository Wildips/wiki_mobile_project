import os
from typing import Literal
from pydantic import BaseModel
from dotenv import load_dotenv
from appium.options.android import UiAutomator2Options
from utils import files


context_type = Literal["local_emulator", "bstack"]


class Settings(BaseModel):
    context: context_type
    login: str = False
    password: str = False
    url: str = False
    app: str = False
    udid: str = False


def session_setup(context):
    if context not in ["local_emulator", "bstack"]:
        raise RuntimeError(f"Неверный тип контекста, возможны значения: {context_type}")

    options = UiAutomator2Options()
    options.set_capability("appWaitActivity", "org.wikipedia.*")

    if context == "local_emulator":
        load_dotenv(dotenv_path=files.abs_project_file_path(f".env.{context}"))
        settings = Settings(
            context=context,
            url=os.getenv("url"),
            udid=os.getenv("udid"),
            app=files.abs_project_file_path(os.getenv("app")),
        )

        options.set_capability("app", settings.app)
        options.set_capability("url", settings.url)
        options.set_capability("udid", settings.udid)

    elif context == "bstack":
        settings = Settings(
            context=context,
            login=os.getenv("login"),
            password=os.getenv("password"),
            url=os.getenv("url"),
            app=os.getenv("app"),
        )
        options.set_capability("platformVersion", "9.0")
        options.set_capability("deviceName", "Google Pixel 3")
        options.set_capability("app", settings.app)
        options.set_capability(
            "bstack:options",
            {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",
                "userName": settings.login,
                "accessKey": settings.password,
            },
        )
    return options, settings
