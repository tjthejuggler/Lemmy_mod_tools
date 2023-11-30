from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import change_banner_if_new_post
import volume_control
import subprocess
import psutil

# Check if the security program is running
def is_running(program):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        # Check if the process name or cmdline matches
        if program in proc.info['name'] or program in ' '.join(proc.info['cmdline']):
            return True
    return False

async def start(update, context):
    await update.message.reply_text('Hello! Send me a command.')

async def echo(update, context):
    received_text = update.message.text
    current_volume = "10"
    security_program = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_security_cam.py'
    security_is_running = is_running(security_program)
    print(f"Received text: {received_text}")
    if received_text.lower() == "u":
        await update.message.reply_text("Updating banner...")
        change_banner_if_new_post.update_banner_if_new_post()
        await update.message.reply_text("Banner updated successfully!")
    if received_text.lower() == "v":
        #get computer volume
        current_volume = volume_control.get_volume()
        print(current_volume)
    if received_text.lower() == "s":        
        if security_is_running:
            # If it is running, kill it
            subprocess.run(["pkill", "-f", security_program], check=True)
        else:
            # If it isn't, start it
            subprocess.Popen(["python", security_program])

    await update.message.reply_text(received_text+"\nu - update banner\nv - toggle volume("+current_volume+")\ns - toggle security program(")


def main():
    with open('/home/lunkwill/projects/Lemmy_mod_tools/secrets/telegram_lunkstealth_bot_auth.txt', 'r') as f:
        token = f.read()

    bot = Bot(token)  # Create a Bot instance

    # Build the application
    application = ApplicationBuilder().token(token).build()

    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the application
    application.run_polling()

if __name__ == '__main__':
    main()
