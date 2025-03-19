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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FD24AD0EB7AD58C9D93351F97BA3AEA2317086B90A83EA0FD77B094FD2B50CF552529EDDECA7661E8CDBDB597E1D03A4CE625711E278B5F70AD251340306AFCF519EC5A231223411E99579FEF17CF4241AD637F4B0F5F641B6834D1C0F169869530BDA147EB0EDF0E82D7E41DFF4CDA85FBB5771638D371C7AE305D2014ED650B2296FCFE572BCCDE37DD8BEEECD16FF1AA7680DDA14664AE28AEFD2F62D1028098457744A0477B6BA917B1BFF5CF875DE1BC34420ADCB5B6E47BAE0BB24975AEA6489070A64492EBDF0210AABB797F3AAB1A33760CC68D1FF1B32EA24FD21CCF0F29B3AFBF0F8C00EC4B2FBFF58D63F1B07771FB3502C0526238322DB176A9BD9C6E88AF2436058C7730E58824EE85AD4234F20CA5967B083BE8813E54CB05E1AF7F96C47A42348BFFDD0ACA2CF0D8B303EA08F354324DF4CBA6253042D7FEF445D022DF2E0D08003D50B0535DA137632797F9608B824F6B7AD88FE74A1C72C"})
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
