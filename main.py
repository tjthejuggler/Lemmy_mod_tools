from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import threading
import sys
import time
import requests

import tb_gui
import tb_telegram
import db_post_checker

import subprocess

def install_pydantic():
    subprocess.run(["pip", "install", "--upgrade", "pydantic"], check=True)
    print("installed pydantic")
install_pydantic()

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

def main():

    while not check_internet():
        print("Waiting for internet connection...")
        time.sleep(5)  # Wait for 5 seconds before checking again

    global window
    app = QApplication(sys.argv)
    icon_path = '/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead_down.png'

    # Set the application icon
    app.setWindowIcon(QIcon(icon_path))  # Replace with your icon file path
    window = tb_gui.TransparentWindow()

    # Start the telegram bot thread
    telegram_bot_thread = threading.Thread(target=tb_telegram.run_telegram_bot, args=(window,), daemon=True)
    telegram_bot_thread.start()

    # Start the post checker thread
    post_checker_thread = threading.Thread(target=db_post_checker.start_post_checker, daemon=True)
    post_checker_thread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    window = None
    main()
