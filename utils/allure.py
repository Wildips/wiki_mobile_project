import allure
import config
import requests
from selene import browser


def attach_bstack_video(session_id):
    bstack_session = requests.get(
        f"https://api.browserstack.com/app-automate/sessions/{session_id}.json",
        auth=(config.LOGIN_MOBILE, config.PASSWORD_MOBILE),
    ).json()
    video_url = bstack_session["automation_session"]["video_url"]

    allure.attach(
        "<html><body>"
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        "</video>"
        "</body></html>",
        name="video recording",
        attachment_type=allure.attachment_type.HTML,
    )


def attach_bstack_screenshot():
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG,
    )


def attach_bstack_page_source():
    allure.attach(
        browser.driver.page_source,
        name="screen xml dump",
        attachment_type=allure.attachment_type.XML,
    )
