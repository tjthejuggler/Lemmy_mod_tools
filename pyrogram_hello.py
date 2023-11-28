import asyncio
from pyrogram import Client

api_id = 28565373
api_hash = "dad789423430505007d4dfc48192b9ce"


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")


asyncio.run(main())


# from pyrogram import Client

# api_id = 28565373
# api_hash = "dad789423430505007d4dfc48192b9ce"

# app = Client("my_account", api_id=api_id, api_hash=api_hash)

# app.run()