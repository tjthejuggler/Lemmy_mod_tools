from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
# from telegram import Bot
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
# import volume_control
# import subprocess
# import psutil
# import asyncio
import threading
import sys

# import change_banner_if_new_post
# import change_db_icon
import volume_control
import tb_gui
import tb_telegram

security_program = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_security_cam.py'
security_program_running = False

def main():
    global window
    app = QApplication(sys.argv)

    icon_path = '/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead_down.png'

    # Set the application icon
    app.setWindowIcon(QIcon(icon_path))  # Replace with your icon file path

    window = tb_gui.TransparentWindow()
    telegram_bot_thread = threading.Thread(target=tb_telegram.run_telegram_bot, args=(window,), daemon=True)
    telegram_bot_thread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    window = None
    main()
