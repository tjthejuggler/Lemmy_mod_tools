from pyrogram import Client

#i will only get notifications from this if the bot is currently running on the computer
def send_telegram_text_as_me_to_bot(message):
    app = Client("my_account")
    async def main():
        async with app:
            await app.send_message("lunkstealth_bot", message)
    app.run(main())

#send_telegram_text_as_me_to_bot("wussup?!")