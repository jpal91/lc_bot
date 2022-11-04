import os
import sys
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Chrome:
    def __init__(self, drive_path) -> None:
        self.drive_path = drive_path
        self.driver = None
        self.options = Options()
    
    def create_client(self, headless = False, args = None):      
        # self.options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if headless or args:
            self.options.headless = headless

            for a in args:
                if a == 'detach':
                    self.options.add_experimental_option('detach', True)
                else:
                    self.options.add_argument(a)

            self.driver = webdriver.Chrome(executable_path="C:\\Users\\User1\\OneDrive\\Desktop\\chromedriver", options=self.options)
        else:
            self.driver = webdriver.Chrome(self.drive_path)
        
        self.driver.implicitly_wait(10)
    
    def go_to(self, url):
        self.driver.get(url)

        time.sleep(15)
        self.close()
    
    def close(self):
        """
        Summary
        Closes the WebDriver once we're done with it.

        Paramters: None

        Returns: None
        """
        self.driver.close()
        return

if __name__ == '__main__':
    load_dotenv()

    d_path = os.getenv('DRIVE_PATH')
    headless = False
    args = []

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == 'headless':
                headless = True
            elif arg == 'user-data':
                p = os.getenv('USER_DATA')
                args.append(f'--user-data-dir={p}')
            else:
                args.append(arg)
    
    driver = Chrome(d_path)
    driver.create_client(headless, args)
    driver.go_to('https://leetcode.com')
    


# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')