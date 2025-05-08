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
    browser.add_cookie({"name": "MUSIC_U", "value": "0015A88DDF729BD8D6E10E4E5C7FC74B0AFA1F71EAB70889D7FA43585A1ED8E9EDE32BC3CECEF5330B337FCB1BEC6BF88D201E1ACF2F1715C6AF0A8F443434A61936102E601FFD55B246F5E9FEFA16E6BE58A8BD4597A60BDD55E6EB750136FAFD6517ACAD466096D844A09B376C5865754C7FB8C0CD06F09EBFD7F36C12903F5D302F2BCDD90E10A37D87787B6DC55486F84616562930DA2F68CFAFEB3E40A57C727A2AF1E5327A867883F6F7E4BA5C50CCEF5BF2C9701363F7A13D0F04C748983BD65D41527C1551109A10FE549E552B1A8D4F9DAEB7941F8647B462175139F927CC9697B24D3A8BB1113A4D418EFC2364EB36C0B7FCD2373D26B5389C44BCE2C1C79CDD33E189B159659B42E98B95AC975E79C0F03F47D34967ADB6279CECD1E94DA45DE08D66A587DFB332AF618243E154AA8ED457AFE97C83982754296BF7A7D05AD5CCB55760A4FF191B0B449ED43FB0BE8CB8CE7F74982BA1A3647B52A8"})
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
