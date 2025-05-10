import os

import allure
from allure_commons.types import AttachmentType
from dotenv import load_dotenv

load_dotenv()
selenoid_url = os.getenv("SELENOID_URL")

def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')

def attach_screenshot(browser):
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG
    )

def add_logs(browser):
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser')) # достаем логи из драйвера, вытягивает из console(бразуер)
    allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')


def add_html(browser):
    html = browser.driver.page_source #верни мне source страницы, выдаст кусок сайта финального шага
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')


def add_video(browser):
    #video_url = "http://00.000.00.00:0000/videos" + browser.driver.session_id + ".mp4" #ссылка на сам файл. формируется при каждом запуске теста
    video_url = selenoid_url + "videos" + browser.driver.session_id + ".mp4"  # ссылка на сам файл. формируется при каждом запуске теста
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>" #плеер HTML
    allure.attach(html, 'video_' + browser.driver.session_id, AttachmentType.HTML, '.html') # далее выдаем ссылку и html код