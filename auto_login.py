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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A05AE7C6EEFD4767F2ECB11C9841D0D7B5D14DE6CD4DD3AB22DEED08242AFB8531F1FFEE0D8C17219C0C450E8A9E5931F61CF3A4FF88A21E571838CF6FDEB426BC2176C9A834994A9B83DFB0B7B2C3CC8D5D913C1DF19D6C2A6B1BE91861997591D9A7989CA88FF380D9A5006CD0AE0DC94F10D2CED5481952A5969418EC9D9ECAA565ED910318BF01928833D10F49CFED3F7EBB7B2C01C21CAE2F76D3542009A409C021A03C4CAA2AC30DD52A30645D316A93AE31EC226252DFAEBF9C29D4EF725FDE10599330A5BD6146FA35B0D45AD83ED97CA732077B2AEFEF183FB2B5EF8B1875A091C8EEE93971152C5E8EB8E10DE3CA3A5796D86EF801FD57FBB166B9F253C8F4FC0307313B5DAF66D09FEAC8AB377DE499CDA64896729E78274483936BDF89ED1ACA319252F36941DF6EA9B0E25AE655413F1EC0AE6A95A2BD398F256D7F17EE603AA61E88FF31E9CC170CEAD18367365BC467FEB82ED39C14DA4CDFFB0146B1EDA583D18CE3AB4323774436686D611561915595FEEEBAB0892176A518CC6D54CA8B98C6D85776322DF2FA18"})
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
