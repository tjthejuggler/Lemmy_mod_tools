from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QPoint
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import volume_control
import subprocess
import psutil
import asyncio
import threading
import sys

import change_banner_if_new_post
import change_db_icon
import volume_control

class TransparentWindow(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.initUI(image_path)

    def initUI(self, image_path):
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable window transparency
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window decorations

        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio)
        label = QLabel(self)
        label.setPixmap(scaled_pixmap)
        self.resize(scaled_pixmap.width(), scaled_pixmap.height())

        self.close_btn = QPushButton('X', self)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.resize(20, 20)
        self.close_btn.move(self.width() - 50, 40)

        self.minimize_btn = QPushButton('-', self)
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.minimize_btn.resize(20, 20)
        self.minimize_btn.move(self.width() - 75, 40)

        self.text_label = QLabel('Hello! Send me a command.', self)
        self.text_label.move(self.width() - 500, 40)
        #make the text black
        self.text_label.setStyleSheet("color: black;")
        

        self.security_checkbox = QCheckBox('Security Program', self)
        #make the text black
        self.security_checkbox.setStyleSheet("color: black;")
        self.security_checkbox.move(self.width() - 500, 60)
        self.security_checkbox.stateChanged.connect(self.toggle_security_from_gui)

        self.show()
        self.oldPos = self.pos()

    def update_checkbox_state(self, is_running):
        self.security_checkbox.setChecked(is_running)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def toggle_security_from_gui(self, state):
        global security_program_running
        if state == Qt.Checked:
            subprocess.Popen(["python", security_program])
            security_program_running = True
        else:
            result = subprocess.run(["pkill", "-f", security_program])
            if result.returncode == 0:
                security_program_running = False
            else:
                print("No matching processes found or error occurred")



    def update_message(self, text):
        self.text_label.setText(text)

security_program = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_security_cam.py'
security_program_running = False

def is_running(program):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
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

        if window:
            window.update_checkbox_state(security_program_running)
    
    await update.message.reply_text(received_text+"\nu - update banner\nv - toggle volume("+str(volume_control.get_volume())+")\ns - toggle security program(tem_bot")

    # Update GUI
    if window:
        window.update_message("Message received: " + received_text)

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with open('/home/lunkwill/projects/Lemmy_mod_tools/telegram_lunkstealth_bot_auth.txt', 'r') as f:
        token = f.read().strip()

    bot = Bot(token)

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    loop.run_until_complete(application.run_polling(stop_signals=None))
    loop.close()

def main():
    global window
    app = QApplication(sys.argv)

    icon_path = '/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead_icon.png'

    # Set the application icon
    app.setWindowIcon(QIcon(icon_path))  # Replace with your icon file path

    window = TransparentWindow('/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead_icon.png')
    
    telegram_bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    telegram_bot_thread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    window = None
    main()
