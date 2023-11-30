from pyrogram import Client

#these are from here https://core.telegram.org/api/obtaining_api_id
with open ('/home/lunkwill/projects/Lemmy_mod_tools/secrets/telegram_app_id.txt', 'r') as f:
    api_id = f.read()
with open ('/home/lunkwill/projects/Lemmy_mod_tools/secrets/telegram_app_hash.txt', 'r') as f:
    api_hash = f.read()

#this is through @BotFather
with open ('/home/lunkwill/projects/Lemmy_mod_tools/secrets/telegram_lunkstealth_bot_auth.txt', 'r') as f:
    bot_token = f.read()

app = Client(
    "lunkstealth_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

app.run()