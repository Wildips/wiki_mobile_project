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

    def session_setup(self, context):
        if context not in ["local_emulator", "bstack"]:
            raise RuntimeError(
                f"Неверный тип контекста, возможны значения: {context_type}"
            )
        self.context = context

        options = UiAutomator2Options()
        options.set_capability("appWaitActivity", "org.wikipedia.*")

        if context == "local_emulator":
            load_dotenv(dotenv_path=files.abs_project_file_path(f".env.{context}"))
            self.app = files.abs_project_file_path(os.getenv("app"))
            self.url = os.getenv("url")
            self.udid = os.getenv("udid")

            options.set_capability("app", self.app)
            options.set_capability("url", self.url)
            options.set_capability("udid", self.udid)

        elif context == "bstack":
            self.app = os.getenv("app")
            self.login = os.getenv("login")
            self.password = os.getenv("password")

            options.set_capability("platformVersion", "9.0")
            options.set_capability("deviceName", "Google Pixel 3")
            options.set_capability("app", self.app)
            options.set_capability(
                "bstack:options",
                {
                    "projectName": "First Python project",
                    "buildName": "browserstack-build-1",
                    "sessionName": "BStack first_test",
                    "userName": self.login,
                    "accessKey": self.password,
                },
            )

        return options


settings = Settings(context="local_emulator")
