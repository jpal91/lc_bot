import os
import json
import time
import asyncio
from dotenv import load_dotenv
import requests

load_dotenv()


class Instance:
    def __init__(self):
        self.token = os.getenv("DO_AUTH")
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.size = "s-1vcpu-512mb-10gb"
        self.image = "ubuntu-20-04-x64"
        self.id = ""

    async def create(self):
        body = {"size": self.size, "image": self.image, "name": "test-drop", "ssh_keys": ['c2:e4:3c:1d:86:25:8c:19:37:36:a3:4d:1e:9f:f5:e3'], "user_data": ""}

        # with open('user_data.txt') as file:
        #     body['user_data'] = file.read()

        req = requests.post(
            "https://api.digitalocean.com/v2/droplets", headers=self.headers, data=body
        )
        res = json.loads(req.text)
        # print(res)
        self.id = res["droplet"]["id"]

    async def get_droplets(self):
        retries = 10
        while True:
            if not self.id:
                print("No id yet, trying again")
                time.sleep(5)
                continue
            if not retries:
                print("Droplet still hasn't completed, shutting down")
                break

            req = requests.get(
                f"https://api.digitalocean.com/v2/droplets/{self.id}",
                headers=self.headers,
            )
            res = json.loads(req.text)

            if res["droplet"]["status"] == "new":
                if retries == 10: print("Droplet confirmed, waiting for creation to finish")
                retries -= 1
                time.sleep(10)
            else:
                print("Droplet complete")
                break


async def main():
    instance = Instance()

    await asyncio.gather(
        instance.create(),
        instance.get_droplets()
    )
    print("Done")


if __name__ == "__main__":
    asyncio.run(main())

# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.headless = True
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
# apt-get install chromium-chromedriver

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# options = Options()
# options.headless = True
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options = options)

# with open('google.txt', "w") as file:
#         file.write(driver.page_source)
# watch "COLUMNS = ps aux | grep apt"
# watch pgrep [a]pt
# driver.close()