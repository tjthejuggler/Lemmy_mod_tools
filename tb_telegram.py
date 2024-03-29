import volume_control
import subprocess
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests
import time

import change_banner_if_new_post
import change_db_icon

security_program = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_security_cam.py'
security_program_running = False

llm_program = '/home/lunkwill/projects/Lemmy_mod_tools/llm_personal_assistant/main.py'

def run_program(llm_program, received_text):
    result = subprocess.run(["python", llm_program, received_text], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        return result.stdout

async def start(update, context):
    await update.message.reply_text('Hello! Send me a command.')

async def echo(update, context, window):
    print("echo")
    global root, security_program_running

    received_text = update.message.text
    current_volume = "10"
    if received_text.lower() != "v 0":
        #make a sound that indicates a text has been received
        subprocess.run(["paplay", "/home/lunkwill/projects/Lemmy_mod_tools/sounds/black_grouse_notification_mod.wav"], check=True)

    icon_prompt = None
    print(f"Received text: {received_text}")
    if received_text.lower() == ".h" or received_text.lower() == "help":
        response = ("""
    .u - update banner and icon
    .ub - update banner
    .ui - update icon
    .ui bird - update icon with prompt bird
    .uix - update icon and del current prompt
    .v - toggle volume("+str(volume_control.get_volume())+")
    .s - toggle security program
    .x - shutdown laptop
    say anything else and bot responds""")
        await update.message.reply_text(response)
    if received_text.lower() == ".u":
        await update.message.reply_text("Updating icon...")
        #old way
        #icon_prompt = change_db_icon.update_icon_if_new_post()
        #new way
        curl_command = "curl https://us-central1-lemmy-auto-icon.cloudfunctions.net/lemmy_auto_icon"
        process = subprocess.run(curl_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the output and error (if any)
        output = process.stdout.decode('utf-8')
        error = process.stderr.decode('utf-8')

        print("Output:", output)
        if process.returncode != 0:
            print("Error:", error)

        await update.message.reply_text("Icon updated successfully!")

        # await update.message.reply_text("Updating banner...")
        # change_banner_if_new_post.update_banner_if_new_post()
        # await update.message.reply_text("Banner updated successfully!")

        # await update.message.reply_text("Updating banner based on icon...")
        # if len(received_text.split(" ")) > 1:
        #     change_banner_if_new_post.update_banner_if_new_post_based_on_icon(" ".join(received_text.split(" ")[1:]))          
        # else:
        #     change_banner_if_new_post.update_banner_if_new_post_based_on_icon()
        # await update.message.reply_text("Banner based on icon updated successfully!")

    elif received_text.lower().startswith(".ubi"):
        await update.message.reply_text("Updating banner based on icon...")
        if len(received_text.split(" ")) > 1:
            change_banner_if_new_post.update_banner_if_new_post_based_on_icon(" ".join(received_text.split(" ")[1:]))          
        else:
            change_banner_if_new_post.update_banner_if_new_post_based_on_icon()
        await update.message.reply_text("Banner based on icon updated successfully!")

    elif received_text.lower().startswith(".ub"):
        await update.message.reply_text("Updating banner...")
        if len(received_text.split(" ")) > 1:
            change_banner_if_new_post.update_banner_if_new_post(" ".join(received_text.split(" ")[1:]))          
        else:
            change_banner_if_new_post.update_banner_if_new_post()
        await update.message.reply_text("Banner updated successfully!")

    elif received_text.lower().startswith(".ui"):        
        await update.message.reply_text("Updating icon...")
        if len(received_text.split(" ")) > 1:
            icon_prompt = change_db_icon.update_icon_if_new_post(" ".join(received_text.split(" ")[1:]))          
        else:
            if received_text.lower().startswith(".uix"):
                print(".uix")
                icon_prompt = change_db_icon.update_icon_if_new_post("replace")
            else:
                icon_prompt = change_db_icon.update_icon_if_new_post()
        await update.message.reply_text("Icon updated successfully!")
    elif received_text.lower().startswith(".v"):
        try:
            #remove any character that is not a number
            received_text = "".join([c for c in received_text if c.isdigit()])
            volume_control.set_volume(int(received_text))
        except:
            pass
    elif received_text.lower() == ".s":
        security_program_running = not security_program_running
        if security_program_running:
            subprocess.Popen(["python", security_program])
        else:
            subprocess.run(["pkill", "-f", security_program], check=True)

        if window:
            window.update_checkbox_state(security_program_running)
    elif received_text.lower() == ".x":
        #shutdown laptop
        subprocess.run(["shutdown", "-h", "now"], check=True)
    #UNCOMMENTING THIS WILL GET THE BOT TO RESPOND TO ANY MESSAGE, BUT IT SHOULD PROBABLY BE ADJUSTED IN HOW IT IS PERFORMED, I THINK IT IS LEAVING STUFF RUNNING IN THE BACKGROUND THAT IS OVERHEATING THE LAPTOP
    # else:
    #     #subprocess.Popen(["python", llm_program, '"'+received_text+'"'])
    #     if not received_text == "The second hottest post has changed." and not received_text == "Finished generating dr. images" and not received_text == "Daily Backup Failed":
    #         response = run_program(llm_program, received_text)
    #         if response and "########################" in response:
    #             trimmed_response = response.split("########################")[2]
    #             received_text = trimmed_response
    response = ""
    if icon_prompt:
        response = "icon prompt:" + icon_prompt +"\n"
    response += received_text
    await update.message.reply_text(response)

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