from dotenv import load_dotenv
import asyncssh
import asyncio
import sys
from Instance import Instance

load_dotenv()

class ServCon:
    def __init__(self, ip):
        self.ip = ip
    
    async def run_client(self):
        with open('priv_key') as file:
            data = file.read()
        
        try:
            key = asyncssh.import_private_key(data)
        except asyncssh.public_key.KeyImportError as e:
            print(e)

        async with asyncssh.connect(host=self.ip, username='root', client_keys=[key], known_hosts = None) as conn:
            with open('user_data.txt', 'r') as f:
                comms = [l.strip() for l in f.readlines()]

                for line in comms:
                    if not line:
                        break
                    retries = 2
                    complete = False
                    while True:
                        try:
                            await conn.run(line, check = True)
                        except Exception as e:
                            print(e)
                        else:
                            print(f"{line}: Done")
                            complete = True
                            break
                        finally:
                            if not complete:
                                if retries:
                                    retries -= 1
                                    await asyncio.sleep(2)
                                else:
                                    print('Can not complete')
                                    break
                            else:
                                await asyncio.sleep(1)
                                break
                
                conn.close()
                return



async def main():

    instance = Instance()

    await instance.create()
    await instance.get_droplets()
    print("Done")
    ip_add = instance.get_ip()
    await asyncio.sleep(15)
    connect = ServCon(ip_add)
    try:
        await connect.run_client()
    except (OSError, asyncssh.Error) as exc:
        sys.exit('SSH connection failed: ' + str(exc))
    
    sys.exit()

if __name__ == '__main__':
    asyncio.run(main())

    

    

    