from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import change_banner_if_new_post
import change_db_icon
import volume_control
import subprocess
import psutil
import tkinter as tk
import asyncio
import threading

root = None

security_program = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_security_cam.py'
security_program_running = False

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
    print("echo")
    global root, security_program_running

    received_text = update.message.text
    current_volume = "10"

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

        # Call the global function to update the checkbox
        update_checkbox_state()
    
    await update.message.reply_text(received_text+"\nu - update banner\nv - toggle volume("+str(volume_control.get_volume())+")\ns - toggle security program(tem_bot")

def update_checkbox_state():
    global root, security_var, security_program_running
    if root is not None and security_var is not None:
        root.after(0, lambda: security_var.set(security_program_running))

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with open('/home/lunkwill/projects/Lemmy_mod_tools/telegram_lunkstealth_bot_auth.txt', 'r') as f:
        token = f.read().strip()

    bot = Bot(token)

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Disable default signal handling
    loop.run_until_complete(application.run_polling(stop_signals=None))
    loop.close()

def create_gui():
    global root, security_program_running, security_var, security_checkbox
    root = tk.Tk()

    # Set the window icon
    icon_path = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_bot_icon5.png'  # Replace with the path to your icon file
    icon = tk.PhotoImage(file=icon_path)
    root.iconphoto(False, icon)

    def toggle_security_from_gui():
        global security_program_running
        if security_var.get():
            # Start the security program
            subprocess.Popen(["python", security_program])
            security_program_running = True
        else:
            # Stop the security program
            subprocess.run(["pkill", "-f", security_program], check=True)
            security_program_running = False

    root.title("Control Panel")

    security_var = tk.BooleanVar(value=security_program_running)
    security_checkbox = tk.Checkbutton(root, text="Security Program", variable=security_var, command=toggle_security_from_gui)
    security_checkbox.pack()

    root.mainloop()

def main():
    # Start the Telegram bot in a separate thread
    telegram_bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    telegram_bot_thread.start()
    create_gui() # Start the Tkinter GUI in the main thread

if __name__ == '__main__':
    main()
