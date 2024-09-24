from dotenv import load_dotenv
from discord import Intents, Client
import asyncio
import os
import threading
import fb
import ptt
import rent591

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

@client.event
async def on_ready():
    asyncio.create_task(background_task())

async def background_task():
    user1 = await client.fetch_user(908727618826825758)
    user2 = await client.fetch_user(1225120185124393062)
    while True:
        with fb.lock:
            if fb.post is not None:
                await user1.send(fb.post)
                await user2.send(fb.post)
                fb.post = None
        
        with ptt.lock:
            if ptt.post is not None:
                await user1.send(ptt.post)
                await user2.send(ptt.post)
                ptt.post = None

        with rent591.lock:
            if rent591.post is not None:
                await user1.send(rent591.post)
                await user2.send(rent591.post)
                rent591.post = None

        await asyncio.sleep(1)

def main() -> None:
    threading.Thread(target=fb.update_post).start()
    threading.Thread(target=ptt.update_post).start()
    threading.Thread(target=rent591.update_post).start()

    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
