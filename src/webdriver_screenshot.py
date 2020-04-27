import os
import shutil
import uuid

from selenium import webdriver

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
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path={}'.format(self._tmp_folder + '/data-path'))
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir={}'.format(self._tmp_folder))
        chrome_options.add_argument('--disk-cache-dir={}'.format(self._tmp_folder + '/cache-dir'))
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium" 

        return chrome_options      

    def __get_correct_height(self, url, width=1280):
        chrome_options=self.__get_default_chrome_options()
        chrome_options.add_argument('--window-size={}x{}'.format(width, 1024))
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
        driver.quit()
        return height

    def save_screenshot(self, url, filename, width=1280):
        height = self.__get_correct_height(url, width=width)

        chrome_options=self.__get_default_chrome_options()
        chrome_options.add_argument('--window-size={}x{}'.format(width, height))
        chrome_options.add_argument('--hide-scrollbars')

        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        driver.save_screenshot(filename)
        driver.quit()

    def close(self):
        # Remove specific tmp dir of this "run"
        shutil.rmtree(self._tmp_folder)

        # Remove possible core dumps
        folder = '/tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if 'core.headless-chromi' in file_path and os.path.exists(file_path) and os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

 