import os
import shutil
import uuid
import logging

from selenium import webdriver

logger = logging.getLogger()

class WebDriverScreenshot:
    def __init__(self):
        self._tmp_folder = '/tmp/{}'.format(uuid.uuid4())

        if not os.path.exists(self._tmp_folder):
            os.makedirs(self._tmp_folder)

        if not os.path.exists(self._tmp_folder + '/user-data'):
            os.makedirs(self._tmp_folder + '/user-data')

        if not os.path.exists(self._tmp_folder + '/data-path'):
            os.makedirs(self._tmp_folder + '/data-path')

        if not os.path.exists(self._tmp_folder + '/cache-dir'):
            os.makedirs(self._tmp_folder + '/cache-dir')

    def __get_default_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--user-data-dir={}'.format(self._tmp_folder + '/user-data'))
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path={}'.format(self._tmp_folder + '/data-path'))
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir={}'.format(self._tmp_folder))
        chrome_options.add_argument('--disk-cache-dir={}'.format(self._tmp_folder + '/cache-dir'))
        chrome_options.add_argument('--disable-dev-shm-usage')

        chrome_options.binary_location = os.getcwd() + "/bin/chromium" 

        return chrome_options      

    def __get_correct_height(self, url, width=1280):
        chrome_options=self.__get_default_chrome_options()
        chrome_options.add_argument('--window-size={}x{}'.format(width, 1024))
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
        driver.quit()
        return height

    def save_screenshot(self, url, filename, width=1280, height=None):
        if height==None:
            height = self.__get_correct_height(url, width=width)

        chrome_options=self.__get_default_chrome_options()
        chrome_options.add_argument('--window-size={}x{}'.format(width, height))
        chrome_options.add_argument('--hide-scrollbars')

        driver = webdriver.Chrome(chrome_options=chrome_options)
        logger.info('Using Chromium version: {}'.format(driver.capabilities['browserVersion']))
        driver.get(url)
        driver.save_screenshot(filename)
        driver.quit()

    def close(self):
        # Remove specific tmp dir of this "run"
        shutil.rmtree(self._tmp_folder)


 