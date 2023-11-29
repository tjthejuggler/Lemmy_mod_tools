import sys
from pyrogram import Client

# Check if an argument is passed, and use it as the message
if len(sys.argv) > 1:
    message = sys.argv[1]
else:
    message = "Default message"  # You can set a default message here

app = Client("my_account")

async def main():
    async with app:
        await app.send_message("lunkstealth_bot", message)

app.run(main())
