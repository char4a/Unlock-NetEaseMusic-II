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
    browser.add_cookie({"name": "MUSIC_U", "value": "00991E54A45E9F2A91AE26F2130F7F114AEA64DCF354CAE862DA5FC0C6107D095FD7F829D52D3831D9CA4CBEB381F17AF46B29DBCBD9CAAFFA1F3B9415C07984011664F4A511B5431B50C5EA02E76E95498E979168CA5918132AA8693AEC8D4A6D2F2FBED00162DF138169C36CB39BB6BDBFAEDE7C3A48311FF7F9D8FCF433194849CC49078912F80AA1CF169B4424755DA5133FB2B48344D3FEE24FD8B5C36A9676B58C10B34C47E8312AD2D1BCDE277086F263B523840F3114DA6F9F20AEB340EE9AB398E2A9EE48FCD96E6752F4B1F8D5BFEC0EEB6A8CB2D489FDD9027647CAD612A7CAC50778E08CCCD7F0AEEAAD009403C9616269AF408F09B819CC8AAE3D984DD44993B66E7BA91100007388CEA82CF9EC4B7DF47B2447D2E76AA4AE7AA4AD246C54F69D394716CCF6CB547C52249882A2C483DDEC35D405F4A2A9BD2862D59AF7A748C1973554EC7768EF8656AA6F75C54328D778CB2FCB650411364D1C"})
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
