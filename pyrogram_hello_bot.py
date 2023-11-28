from pyrogram import Client

api_id = 28565373
api_hash = "dad789423430505007d4dfc48192b9ce"
bot_token = "6840462381:AAFU8vAOD_eG_44TqFVMNETGZayCydmDvdk"

app = Client(
    "lunkstealth_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

app.run()