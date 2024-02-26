from pyrogram import Client
import asyncio

# #i will only get notifications from this if the bot is currently running on the computer
# async def send_telegram_text_as_me_to_bot(message):
#     app = Client("my_account")
#     async def main():
#         async with app:
#             await app.send_message("lunkstealth_bot", message)
#     app.run(main())

async def send_telegram_text_as_me_to_bot(message):
    # Set up your Pyrogram client here, without calling app.run()
    app = Client("my_account")
    async with app:
        await app.send_message("lunkstealth_bot", message)

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# coro = send_telegram_text_as_me_to_bot("The second activest post has changed.")
# loop.run_until_complete(coro)
