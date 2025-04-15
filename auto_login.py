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
    browser.add_cookie({"name": "MUSIC_U", "value": "008E2AE559518E912DD19C34508481E2281FA036724ED0B67264E9D0C68C8232EC4352987523965AC0C285A0D06119C5940EC41B259487C09457A9D8570050DD98A30613BD5A70F4743604378C3ACABEA00975F92EB0D9237E9E2B3954FBCB325CDE0698A68AEC06697D100B5F43AA9F399A3251F97D0916F6572AC2317A6C3806504EDD28A50FB0154405B29E2C81E8DF8DAC460157EEA51C85EACA95FAF7BEC4BF8E57245316AB0565500D0E94FAD830C06FA6320244F2DEB8F96CA23B4C27F6287235669FD6808BF238F6CC0C3314B7AB93699AA2AD29E6AB69B500ED9E336F1689A97AC7CB4061459112450D8305759D07A3BA1388B80592C95EB85787DFEDB93762040FDAA5645854B1B706973E5FB5589FE729E97F7CEAE55DA288F83AE9816B3BE9A85DFAFE743801AD317232B7187590A899D43A690F4E78E7D64AFA83B0F040B4EFBD09DADECDF51FBB399FF3A0CB9F929C46DB5DFCABD0E252FFB54B"})
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
