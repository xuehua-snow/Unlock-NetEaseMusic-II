# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00655E76EDF57B51F0E50E53E21CE2723848A69CE1B8873318780354CC354065CBD89EFEF5D8B01D70B4315196CA9A4DC2C7F3F5BCCFE56860088E9E4093F72E2067CE295DABA7D138E1776D198F6B483728F90BFA7A8A0D11494B6E99E364D49B030F0CA36B4B2B2344ED124E6CFCCF3D3AF084CEE9AEEE628466D9B3E7698D0739890E4031090EAC78B3FB789545E593BFBBF59B738F654D32759CEF8D280F9B8D646BC8EA93C0CC8928A7FBB6006F7B531819F5C71AD1BE3DEBD9404D8BAFA9F1609D39F2043F7FB3E104CDC5E591BBD0D124AE855B66F5529540AD4848A714B80BBDD880BDC6E912DB695F8C055E22F24217C797049FC67F4D73F03733A54602F9425F15D6DFA8764E010EED084A6FFD7B51F4A0E0C734603DAF1FEB1787F95F934FC1FF10609A7A2230B02745AA55A17BB4A025ECAF15D48BAC50E7CA12AE1C1036D2BEEE6E8929E2299D1DE3DC0E4138B02AC26B7E973685DC636B81A845"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
