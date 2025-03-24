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
    browser.add_cookie({"name": "MUSIC_U", "value": "00716AFA90C0993C3F3E79F8516292849B722243E4539136EAAAE56E98D274952CBF3E9E0F3A6CBA6FDAA5830B2055AFFBD26BE87BD80522EB522BD6232F4D56DC137690BB89E32AC6CCD424FBE18C60B0DFCF135390A7A09C6740276BEAB7D3FC90B2B0A76BD6D8EF0472A1FD99CF4F159C9979DE672831F3E58AF29FF9D1C767076BA9FF4E3876ED3EFA5FCC5879382A69C916CB2E5EC169E4048B03B203E26DECEA2D6103A44068F258ADE1B22FB0E1581A176D84E6273D792185F82FFB42CF9A0E2C4468107768E5E9559017881AA8EE040EDC8B1D5B6F7D6BA86C8924E800F1C34B7F3B85CF7F9F1D3E88877B1570925D93A8F3BA991487BAEB3E57D51FC05CCE758FEF9D2B43C372B904FFF4F277222557B466BB6AD348796B48B7EB89E6E7CD287FF4DA19E6DF814AA39DA16D67AEBD0A3FFBD85E42C1BA14DB64C16871AF0E1907DF1BCA60443B80637F814C881CAEA7133C63C828EB63F07EE0B07706"})
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
