import time
import traceback
from loguru import logger

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from loader import pglt

import os, json

is_headless = True


class Chrome:
    def __init__(self, user, directory='mobile'):
        logger.debug('Инициализирую объект Chrome')

        # Selenium
        os.environ['WDM_LOCAL'] = '1'
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("--no-sandbox")
        self.option.add_argument("--log-level=3")
        # self.option.add_argument("--start-maximized")
        self.option.add_argument("--window-size=1920,1080")
        self.option.add_argument("--disable-gpu")
        self.option.add_argument("--disable-blink-features=AutomationControlled")
        self.option.add_argument(f"user-data-dir={os.getcwd()}/selenium")
        self.option.add_argument(f'user-agent={user}')
        self.option.headless = is_headless  # True - тихий режим (без интерфейса), False - с интерфейсом браузера
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.option)
        self.driver.set_page_load_timeout = 10

    @pglt.time()
    def get_html(self, url):
        start_time = time.time()
        try:
            self.driver.get(url)
            source = self.driver.page_source

        except Exception:
            self.driver.quit()
            del self.driver

            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.option)
            self.driver.get(url)
            source = self.driver.page_source

        time.sleep(3)
        logger.debug(f'The page loaded in {time.time() - start_time}')

        self.driver.save_screenshot('last_screen.png')
        return source

    def quit(self):
        self.driver.quit()
        return 0
