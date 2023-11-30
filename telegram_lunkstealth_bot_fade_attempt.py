from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QSystemTrayIcon, QMenu, QGraphicsOpacityEffect
from PyQt5 import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import volume_control
import subprocess
import psutil
import asyncio
import threading
import sys
from PIL import Image
import os
import random

import change_banner_if_new_post
import change_db_icon
import volume_control

class TransparentWindow(QWidget):
    def __init__(self, image_folder):
        super().__init__()
        self.image_path_icon = '/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead_down.png'
        self.image_folder = image_folder
        self.image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        self.current_image_path = None  # To store the current image path
        self.background_fade_time = 20000
        self.initUI()  # Initialize the UI

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable window transparency
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window decorations
    
        self.setGeometry(100, 100, 640, 480)
        self.setWindowTitle('Fading Background Window')

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
        # Set up the labels for the background images
        self.background_label1 = QLabel(self)
        self.background_label2 = QLabel(self)
        self.background_label1.setGeometry(self.rect())
        self.background_label2.setGeometry(self.rect())

        # Apply opacity effect and set initial opacity
        self.applyOpacityEffect(self.background_label1)
        self.applyOpacityEffect(self.background_label2)
        self.background_label1.graphicsEffect().setOpacity(0)
        self.background_label2.graphicsEffect().setOpacity(0)

        # Set initial opacity of the odd label (background_label1) to 1 (fully visible)
        self.background_label1.graphicsEffect().setOpacity(1)

        # Load the initial image for the odd label
        initial_image_path = random.choice(self.image_files)
        self.updateBackground(self.background_label1, initial_image_path)
        self.current_image_path = initial_image_path  # Store the current image path

        # Initialize and start the timers
        self.odd_timer = QTimer(self)
        self.odd_timer.timeout.connect(self.updateOddBackground)
        self.odd_timer.start(self.background_fade_time)  # 10 seconds for full fade in and fade out cycle

        self.even_timer = QTimer(self)
        self.even_timer.timeout.connect(self.updateEvenBackground)
        QTimer.singleShot(int(self.background_fade_time/2), lambda: self.even_timer.start(self.background_fade_time)) 

        # Create System Tray Icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.image_path_icon))
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Create context menu for tray icon
        self.tray_menu = QMenu()
        restore_action = self.tray_menu.addAction("Restore")
        quit_action = self.tray_menu.addAction("Quit")
        self.tray_icon.setContextMenu(self.tray_menu)

        restore_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(QApplication.quit)

        opaque_style = "background-color: rgba(255, 255, 255, 255);"
        self.close_btn.setStyleSheet(opaque_style)
        self.minimize_btn.setStyleSheet(opaque_style)
        self.text_label.setStyleSheet("color: black; " + opaque_style)
        self.security_checkbox.setStyleSheet("color: black; " + opaque_style)

        self.close_btn.raise_()
        self.minimize_btn.raise_()
        self.text_label.raise_()
        self.security_checkbox.raise_()

        self.tray_icon.show()

    def updateBackground(self, label, image_path):
        
        # Load your image
        image = Image.open(image_path)

        # Convert black pixels to transparent
        image = image.convert("RGBA")
        datas = image.getdata()

        newData = []
        black_tolerance = 30  # Define your tolerance level (0-255)
        for item in datas:
            # Check if a pixel is close enough to black to be made transparent
            if item[0] < black_tolerance and item[1] < black_tolerance and item[2] < black_tolerance:
                newData.append((255, 255, 255, 0))  # Making it transparent
            else:
                newData.append(item)

        image.putdata(newData)
        # Find the bounding box of non-transparent pixels
        bbox = image.getbbox()
        
        # Crop the image to the bounding box
        if bbox:
            image = image.crop(bbox)

        # Save the modified image to use in PyQt
        image.save('temp_image.png', "PNG")

        #image_path = 'temp_image.png'
        # Save the processed image temporarily
        temp_image_path = 'temp_background.png'
        image.save(temp_image_path, "PNG")

        # Update the label pixmap
        pixmap = QPixmap(temp_image_path)
        label.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding))

    def updateOddBackground(self):
        # Choose a random image for the odd background cycle
        next_image_path = random.choice(self.image_files)
        while next_image_path == self.current_image_path:
            next_image_path = random.choice(self.image_files)

        self.current_image_path = next_image_path
        # Set initial opacity of the label to 0 and start the transition
        self.background_label1.graphicsEffect().setOpacity(0)
        # Update background for the odd label (e.g., background_label1)
        self.updateBackground(self.background_label1, self.current_image_path)


        self.animateTransition(self.background_label1)

    def updateEvenBackground(self):
        # Choose a random image for the even background cycle
        next_image_path = random.choice(self.image_files)
        while next_image_path == self.current_image_path:
            next_image_path = random.choice(self.image_files)

        self.current_image_path = next_image_path
        # Set initial opacity of the label to 0 and start the transition
        self.background_label2.graphicsEffect().setOpacity(0)
        # Update background for the even label (e.g., background_label2)
        self.updateBackground(self.background_label2, self.current_image_path)


        self.animateTransition(self.background_label2)

    def changeBackground(self):
        # Randomly select the next image, different from the current one
        next_image_path = random.choice(self.image_files)
        while next_image_path == self.current_image_path:
            next_image_path = random.choice(self.image_files)

        self.current_image_path = next_image_path  # Update the current image path

        next_label = self.background_label2 if self.background_label1.isVisible() else self.background_label1
        #self.updateBackground(next_label, self.current_image_path)

        # Set initial opacity of the next label to 0
        next_label.graphicsEffect().setOpacity(0)

        self.animateTransition(next_label)


    def applyOpacityEffect(self, widget):
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)
        return opacity_effect


    def animateTransition(self, next_label):
        current_label = self.background_label1 if next_label == self.background_label2 else self.background_label2

        # Ensure opacity effects are applied
        self.applyOpacityEffect(current_label)
        self.applyOpacityEffect(next_label)

        half_cycle_duration = self.background_fade_time // 2  # Half of the full cycle

        # Setup fade-in for the next label (first half of the cycle)
        self.fade_in = QPropertyAnimation(next_label.graphicsEffect(), b"opacity")
        self.fade_in.setDuration(half_cycle_duration)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)

        # Setup fade-out for the next label (second half of the cycle)
        self.fade_out_next = QPropertyAnimation(next_label.graphicsEffect(), b"opacity")
        self.fade_out_next.setDuration(half_cycle_duration)
        self.fade_out_next.setStartValue(1)
        self.fade_out_next.setEndValue(0)

        # Start fade-in immediately
        self.fade_in.start()
        # Schedule fade-out to start after fade-in completes
        QTimer.singleShot(half_cycle_duration, self.fade_out_next.start)

        # If needed, handle the current label's fade-out here
        # (Assuming the current label is already fully visible when this function is called)
        self.fade_out_current = QPropertyAnimation(current_label.graphicsEffect(), b"opacity")
        self.fade_out_current.setDuration(half_cycle_duration)
        self.fade_out_current.setStartValue(1)
        self.fade_out_current.setEndValue(0)
        self.fade_out_current.start()


    def tray_icon_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_window()

    def show_window(self):
        self.showNormal()
        self.activateWindow()

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

    def closeEvent(self, event):
        # Minimize to system tray instead of exiting
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Application Minimized", "Your application is still running.", QIcon(self.image_path_icon))

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

    with open('/home/lunkwill/projects/Lemmy_mod_tools/secrets/telegram_lunkstealth_bot_auth.txt', 'r') as f:
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

    icon_path = '/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead_down.png'

    # Set the application icon
    app.setWindowIcon(QIcon(icon_path))  # Replace with your icon file path

    window = TransparentWindow('/home/lunkwill/projects/Lemmy_mod_tools/backgrounds')
    window.show()
    
    telegram_bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    telegram_bot_thread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    window = None
    main()
