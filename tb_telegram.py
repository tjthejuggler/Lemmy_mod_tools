import volume_control
import subprocess
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import change_banner_if_new_post
import change_db_icon

security_program = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_security_cam.py'
security_program_running = False

async def start(update, context):
    await update.message.reply_text('Hello! Send me a command.')

async def echo(update, context, window):
    print("echo")
    global root, security_program_running

    received_text = update.message.text
    current_volume = "10"

    #make a sound that indicates a text has been received
    subprocess.run(["paplay", "/home/lunkwill/projects/Lemmy_mod_tools/sounds/black_grouse_notification_mod.wav"], check=True)

    print(f"Received text: {received_text}")
    if received_text.lower() == "u":
        await update.message.reply_text("Updating banner...")
        change_banner_if_new_post.update_banner_if_new_post()
        await update.message.reply_text("Banner updated successfully!")
        await update.message.reply_text("Updating icon...")
        change_db_icon.update_icon_if_new_post()
        await update.message.reply_text("Icon updated successfully!")
    elif received_text.lower() == "ub":
        await update.message.reply_text("Updating banner...")
        change_banner_if_new_post.update_banner_if_new_post()
        await update.message.reply_text("Banner updated successfully!")
    elif received_text.lower() == "ui":        
        await update.message.reply_text("Updating icon...")
        change_db_icon.update_icon_if_new_post()
        await update.message.reply_text("Icon updated successfully!")
    elif received_text.lower().startswith("v"):
        try:
            volume_control.set_volume(int(received_text[2:]))
        except:
            pass
    elif received_text.lower() == "s":
        security_program_running = not security_program_running
        if security_program_running:
            subprocess.Popen(["python", security_program])
        else:
            subprocess.run(["pkill", "-f", security_program], check=True)

        if window:
            window.update_checkbox_state(security_program_running)
    
    await update.message.reply_text(received_text+"\nu - update banner\nv - toggle volume("+str(volume_control.get_volume())+")\ns - toggle security program(tem_bot")

    # Update GUI
    if window:
        window.update_message("Message received: " + received_text)

def run_telegram_bot(window):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with open('/home/lunkwill/projects/Lemmy_mod_tools/secrets/telegram_lunkstealth_bot_auth.txt', 'r') as f:
        token = f.read().strip()

    bot = Bot(token)

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: echo(update, context, window)))

    loop.run_until_complete(application.run_polling(stop_signals=None))
    loop.close()