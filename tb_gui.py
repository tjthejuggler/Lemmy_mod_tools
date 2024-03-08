from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QSystemTrayIcon, QMenu, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QPoint, QTimer, QSize, QDateTime, pyqtSignal
from PIL import Image, ImageFilter
from PyQt5.QtWidgets import QMessageBox, QApplication

import os
import random
import subprocess
import json

import asyncio
import telegram_service
import time

import pyqt5_dialog
import threading
import psutil


print('Starting tb_gui.py')

security_program = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_security_cam.py'

def notify(message):
    msg = "notify-send ' ' '"+message+"'"
    os.system(msg)

class TransparentWindow(QWidget):
    # Define a signal for starting the timer dialog
    startTimerDialogSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.startTimerDialogSignal.connect(self.start_timer_dialog)
        #self.icon_image_path = '/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead_down.png'
        self.label = QLabel(self)  # Label to display the background image
        with open('/home/lunkwill/projects/Lemmy_mod_tools/current_background.txt', 'r') as f:
            self.icon_image_path = f.read()
        self.load_random_background(self.icon_image_path)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tooltip)
        self.timer.start(1000)  # Update every second
        self.timer_tooltip = QTimer(self)
        self.timer_tooltip.timeout.connect(self.set_random_tooltip)
        self.timer_tooltip.start(30000)  # Update every second               
        self.initUI()        
        self.show()

    def update_tooltip(self):
        if self.timer_start_time != 0:

            start_time = QDateTime.fromSecsSinceEpoch(int(self.timer_start_time))
            elapsed_time = QDateTime.currentDateTime().toSecsSinceEpoch() - start_time.toSecsSinceEpoch()
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            cur_type = self.current_timer_type
            self.tray_icon.setToolTip(f"{cur_type}\n{int(hours):02}:{int(minutes):02}:{int(seconds):02}")

    def load_random_background(self, image_path_given=None):
        # Load a new random image from the backgrounds folder
        if image_path_given:
            image_path = image_path_given
        else:
            backgrounds_dir = '/home/lunkwill/projects/Lemmy_mod_tools/backgrounds/'
            backgrounds_list = os.listdir(backgrounds_dir)
            #remove black_behind.png from backgrounds_list
            backgrounds_list.remove("black_behind3.png")
            random_background = random.choice(backgrounds_list)
            image_path = os.path.join(backgrounds_dir, random_background)

        self.icon_image_path = image_path
        #save this path to a file
        with open('/home/lunkwill/projects/Lemmy_mod_tools/current_background.txt', 'w') as f:
            f.write(image_path)
        image = Image.open(image_path)
        print(image_path)
        # Process the image
        image = image.convert("RGBA")
        newData = []
        black_tolerance = 20
        for item in image.getdata():
            if item[0] < black_tolerance and item[1] < black_tolerance and item[2] < black_tolerance:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        
        # Create an image object with the data
        processed_image = Image.new("RGBA", image.size)
        processed_image.putdata(newData)

        # Apply the median filter repeatedly
        for _ in range(3):  # change the range as necessary
            processed_image = processed_image.filter(ImageFilter.MedianFilter(size=3))

        #put this image in front of "/home/lunkwill/projects/Lemmy_mod_tools/black_behind.png"
        black_behind = Image.open("/home/lunkwill/projects/Lemmy_mod_tools/backgrounds/black_behind3.png")
        #make black_behind the same size as image
        black_behind = black_behind.resize(processed_image.size)
        black_behind.paste(processed_image, (0, 0), processed_image)
        processed_image = black_behind
        bbox = processed_image.getbbox()
        if bbox:
            #make the bbox slightly bigger on all sides
            bbox = (bbox[0]-10, bbox[1]-10, bbox[2]+10, bbox[3]+10)
            processed_image = processed_image.crop(bbox)
        # Save the modified image
        processed_image.save('temp_image.png', "PNG")
        # Set the new image as the window background
        self.set_background_image('temp_image.png')

    # def set_background_image(self, image_path):
    #     pixmap = QPixmap(image_path)
    #     scaled_pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio)
    #     self.label.setPixmap(scaled_pixmap)
    #     self.resize(scaled_pixmap.width(), scaled_pixmap.height())
    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        # Define maximum window size
        max_window_size = QSize(800, 800)
        # Scale pixmap while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(max_window_size, Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_pixmap)
        # Resize window to fit the scaled image
        self.resize(scaled_pixmap.width(), scaled_pixmap.height())

    def start_timer_dialog(self, type):
        time.sleep(5)
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Start Timer')
        msgBox.setText(f'Do you want to start a timer for {type}?')
        yesButton = msgBox.addButton('Yes', QMessageBox.YesRole)
        noButton = msgBox.addButton('No', QMessageBox.NoRole)
        result = msgBox.exec()
        # Check if the window is still open before proceeding
        if self.isVisible():
            print('result:', result)
            if result == 0:
                self.startTimer(type)
                print(f'Starting timer for {type}.')
                # Here you can add the code to start the timer
            else:
                print("No clicked.")
            # Explicitly delete the QMessageBox
            msgBox.deleteLater()
        else:
            print("Window is closed. Operation cancelled.")

    def check_program(self):
        drawio_was_open = False
        vscode_was_open = False
        while True:
            drawio_is_open = False
            vscode_is_open = False
            # Check if the specific programs are running
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'drawio':
                    drawio_is_open = True
                elif proc.info['name'] == 'code':
                    vscode_is_open = True

            # If drawio is newly opened, start the timer dialog
            # if drawio_is_open and not drawio_was_open:
            #     self.start_timer_dialog('writing')  # Replace 'your_argument' with the actual argument

            # If drawio is newly opened, start the timer dialog
            if drawio_is_open and not drawio_was_open:
                self.startTimerDialogSignal.emit('writing')
            # If VS Code is newly opened, start the timer dialog
            if vscode_is_open and not vscode_was_open:
                self.startTimerDialogSignal.emit('programming')
            # # If VS Code is newly opened, start the timer dialog
            # if vscode_is_open and not vscode_was_open:
            #     self.start_timer_dialog('programming')  # Replace 'your_argument' with the actual argument

            drawio_was_open = drawio_is_open
            vscode_was_open = vscode_is_open

            time.sleep(1)  # Wait for a second before checking again

    # def my_close(self):
    #     self.set_random_tooltip()
    #     self.close()

    def set_random_tooltip(self):
        self.tray_icon.setToolTip(self.get_random_myremind())
        self.tray_icon.show()

    def initUI(self):

        self.thread = threading.Thread(target=self.check_program)
        self.thread.daemon = True
        self.thread.start()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        #Create the close button
        self.close_btn = QPushButton('X', self)
        self.close_btn.clicked.connect(self.close)

        self.close_btn.resize(50, 50)
        self.close_btn.move(int(self.width()/2)-25, 500)

        # Initialize close timer
        self.close_timer = QTimer()
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self.quit_application)
        self.close_timer.setInterval(2000)  # Set the timer for 2 seconds

        # Modify the close button events
        self.close_btn.mousePressEvent = self.start_close_timer
        self.close_btn.mouseReleaseEvent = self.stop_close_timer

        # Style for the close button
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: transparent;
                border: none;
                font-size: 76px;
            }
            QPushButton:hover {
                color: red;
            }
        """)

        #create the dialog input button
        self.dialog_btn = QPushButton('<', self)
        self.dialog_btn.clicked.connect(self.open_dialog)
        self.dialog_btn.resize(50, 50)
        self.dialog_btn.move(int(self.width()/2)+125, 300)

        self.dialog_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                                    color: transparent;
                                    border: none;
                                    font-size: 76px;
            }
            QPushButton:hover {
                color: green;
            }
        """)

        #two bu
        self.upvote_button = QPushButton('+', self)
        self.upvote_button.clicked.connect(self.upvote_art)
        self.upvote_button.resize(50, 50)
        self.upvote_button.move(int(self.width()/2)-155, 300)

        self.upvote_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                                    color: transparent;
                                    border: none;
                                    font-size: 76px;
            }
            QPushButton:hover {
                color: blue;
            }
        """)

        self.upvote_button = QPushButton('-', self)
        self.upvote_button.clicked.connect(self.downvote_art)
        self.upvote_button.resize(50, 50)
        self.upvote_button.move(int(self.width()/2)-110, 300)

        self.upvote_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                                    color: transparent;
                                    border: none;
                                    font-size: 76px;
            }
            QPushButton:hover {
                color: white;
            }
        """)

        self.text_label = QLabel('Hello! Send me a command.', self)
        self.text_label.move(self.width() - 500, 40)
        #make the text black
        self.text_label.setStyleSheet("color: black;")
        
        self.security_checkbox = QCheckBox('Security Program', self)
        #make the text black
        self.security_checkbox.setStyleSheet("color: black;")
        self.security_checkbox.move(self.width() - 500, 60)
        self.security_checkbox.stateChanged.connect(self.toggle_security_from_gui)
        
        self.oldPos = self.pos()
        #IS BACKGROUND SIZE GETTING SET AT THE BEGINNING? IT SHOULD BE ABLE TO CHANGE SIZE

        self.timer_start_time = 0
        self.current_timer_type = ""

        # System tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.icon_image_path))
        

        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_menu = QMenu()
        stop_timer_action = self.tray_menu.addAction("STOP Timer")
        program_timer_action = self.tray_menu.addAction("Program Timer")
        writing_timer_action = self.tray_menu.addAction("Writing Timer")
        reading_timer_action = self.tray_menu.addAction("Reading Timer")
        podcast_timer_action = self.tray_menu.addAction("Podcast Timer")
        drawing_timer_action = self.tray_menu.addAction("Drawing Timer")

        freestyle_juggling_timer_action = self.tray_menu.addAction("Freestyle Juggling Timer")
        
        restore_action = self.tray_menu.addAction("Restore")
        quit_action = self.tray_menu.addAction("Quit")
        self.tray_icon.setContextMenu(self.tray_menu)
        stop_timer_action.triggered.connect(lambda: self.stopTimer("stopping"))
        program_timer_action.triggered.connect(lambda: self.startTimer("programming"))
        writing_timer_action.triggered.connect(lambda: self.startTimer("writing"))
        reading_timer_action.triggered.connect(lambda: self.startTimer("reading"))
        podcast_timer_action.triggered.connect(lambda: self.startTimer("podcast"))
        drawing_timer_action.triggered.connect(lambda: self.startTimer("drawing"))
        freestyle_juggling_timer_action.triggered.connect(lambda: self.startTimer("freestyle_juggling"))
        
        restore_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(QApplication.quit)

        self.set_random_tooltip()
        self.tray_icon.show()

    def startTimer(self, message):
        print(message)
        self.timer_start_time = time.time()
        self.current_timer_type = message
        #self.update_message("Timer started")
        #self.update_checkbox_state(True)

    def get_random_myremind(self):
        with open('/home/lunkwill/Documents/obsidyen/MyReminds.md', 'r') as file:
            content = file.read()
        items = content.split('\n\n')  # Split the content by empty lines
        random_myremind = random.choice(items)  # Select a random item
        return random_myremind
    
    def stopTimer(self, message):
        print(message)
        if self.current_timer_type != "" and self.timer_start_time != 0:
            elapsed_time = time.time() - self.timer_start_time
            pyqt5_dialog.ask_log_time(elapsed_time, self.current_timer_type)

            #create a popup question to ask if the time should be logged


            #self.update_message("Timer stopped")
            #self.update_checkbox_state(False)
        elapsed_time = time.time() - self.timer_start_time

        self.timer_start_time = 0
        #/home/lunkwill/Documents/obsidyen/MyReminds.md

        self.set_random_tooltip()
        #create a popup question
        #self.update_message("Timer stopped")
        #self.update_checkbox_state(False)


    def open_dialog(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your text:')
        
        if ok:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            coro = telegram_service.send_telegram_text_as_me_to_bot(text)
            loop.run_until_complete(coro)

        self.set_random_tooltip() #just get a random my_remind item as the hover of the syste tray icon

    def upvote_art(self):
        with open('/home/lunkwill/projects/Lemmy_mod_tools/bot_art_upvotes.txt', 'r') as f:
            art_votes_dict = json.load(f)
        if self.icon_image_path not in art_votes_dict:
            art_votes_dict[self.icon_image_path] = 1
        else:
            art_votes_dict[self.icon_image_path] += 1
        with open('/home/lunkwill/projects/Lemmy_mod_tools/bot_art_upvotes.txt', 'w') as f:
            json.dump(art_votes_dict, f)
        self.load_random_background()
        notify("upvoted")

        self.set_random_tooltip() #just get a random my_remind item as the hover of the syste tray icon

    def downvote_art(self):
        with open('/home/lunkwill/projects/Lemmy_mod_tools/bot_art_downvotes.txt', 'r') as f:
            art_votes_dict = json.load(f)
        if self.icon_image_path not in art_votes_dict:
            art_votes_dict[self.icon_image_path] = 1
        else:
            art_votes_dict[self.icon_image_path] += 1
        with open('/home/lunkwill/projects/Lemmy_mod_tools/bot_art_downvotes.txt', 'w') as f:
            json.dump(art_votes_dict, f)
        #move it to rejected_backgrounds
        os.rename(self.icon_image_path, '/home/lunkwill/projects/Lemmy_mod_tools/rejected_backgrounds/'+self.icon_image_path.split('/')[-1])
        #reopen a new background
        self.load_random_background()       
        notify("rejected")   

        self.set_random_tooltip() #just get a random my_remind item as the hover of the syste tray icon

    def start_close_timer(self, event):
        self.close_timer.start()  # Start the 2-second timer
        QPushButton.mousePressEvent(self.close_btn, event)  # Call original event

    def stop_close_timer(self, event):
        if self.close_timer.isActive():
            self.close_timer.stop()  # Stop the timer if it's still running
            self.hide()  # Minimize to system tray
        QPushButton.mouseReleaseEvent(self.close_btn, event)  # Call original event

    def quit_application(self):
        QApplication.quit()  # Quit the application

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.MiddleClick:
            QApplication.quit()  # Quit the application on middle-click
        elif reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_window()

    def show_window(self):
        self.load_random_background()  # Load a new background every time the window is shown
        self.showNormal()
        self.activateWindow()

    # def toggle_security_from_gui(self, state):
    #     if state == Qt.Checked:
    #         subprocess.Popen(["python", security_program])
    #     else:
    #         subprocess.run(["pkill", "-f", security_program])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

            self.set_random_tooltip() #just get a random my_remind item as the hover of the syste tray icon

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

        self.set_random_tooltip() #just get a random my_remind item as the hover of the syste tray icon

    def update_checkbox_state(self, is_running):
        self.security_checkbox.setChecked(is_running)

        self.set_random_tooltip() #just get a random my_remind item as the hover of the syste tray icon

    def closeEvent(self, event):
        # Minimize to system tray instead of exiting
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Application Minimized", "Your application is still running.", QIcon(self.icon_image_path))
