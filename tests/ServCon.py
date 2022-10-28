from dotenv import load_dotenv
import asyncssh
import asyncio
import sys

load_dotenv()

class ServCon:
    def __init__(self):
        self.ip = '159.65.116.235'
    
    async def run_client(self):
        with open('priv_key') as file:
            data = file.read()
        
        try:
            key = asyncssh.import_private_key(data)
        except asyncssh.public_key.KeyImportError as e:
            print(e)

        async with asyncssh.connect(host=self.ip, username='root', client_keys=[key], known_hosts = None) as conn:
            # result = await conn.run('ls /bin', check = True)
            # print(result.stdout, end = '')
            with open('user_data.txt', 'r') as f:
                comms = f.readlines()

                for line in comms:
                    await conn.run(line, check = True)

connect = ServCon()

try:
    asyncio.get_event_loop().run_until_complete(connect.run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))