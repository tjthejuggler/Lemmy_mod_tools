import asyncio
from pyrogram import Client

#these are from here https://core.telegram.org/api/obtaining_api_id
with open ('/home/lunkwill/projects/Lemmy_mod_tools/telegram_app_id.txt', 'r') as f:
    api_id = f.read()
with open ('/home/lunkwill/projects/Lemmy_mod_tools/telegram_app_hash.txt', 'r') as f:
    api_hash = f.read()

async def main():
    async with Client("my_account", api_id, api_hash) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")


asyncio.run(main())

