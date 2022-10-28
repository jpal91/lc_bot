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
        body = {"size": self.size, "image": self.image, "name": "test-drop", "ssh_keys": ['01:fe:81:3e:16:07:d8:85:ce:99:e9:ab:de:04:2d:d9'], "user_data": ""}

        with open('user_data.txt') as file:
            body['user_data'] = file.read()

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

