from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QCheckBox, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QPoint
from PIL import Image
import os
import random
import subprocess

print('Starting tb_gui.py')

security_program = '/home/lunkwill/projects/Lemmy_mod_tools/telegram_security_cam.py'

class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.icon_image_path = '/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead_down.png'
        self.label = QLabel(self)  # Label to display the background image
        self.load_random_background()  # Load the initial background
        self.initUI()
        
        self.show()

    def load_random_background(self):
        # Load a new random image from the backgrounds folder
        backgrounds_dir = '/home/lunkwill/projects/Lemmy_mod_tools/backgrounds/'
        backgrounds_list = os.listdir(backgrounds_dir)
        #remove black_behind.png from backgrounds_list
        backgrounds_list.remove("black_behind3.png")
        random_background = random.choice(backgrounds_list)

        image_path = os.path.join(backgrounds_dir, random_background)
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
        image.putdata(newData)
        #put this image in fron of "/home/lunkwill/projects/Lemmy_mod_tools/black_behind.png"
        black_behind = Image.open("/home/lunkwill/projects/Lemmy_mod_tools/backgrounds/black_behind3.png")
        #make black_behind the same size as image
        black_behind = black_behind.resize(image.size)
        black_behind.paste(image, (0, 0), image)
        image = black_behind    

        
        bbox = image.getbbox()
        if bbox:
            #make the bbox slightly bigger on all sides
            bbox = (bbox[0]-10, bbox[1]-10, bbox[2]+10, bbox[3]+10)
            image = image.crop(bbox)

        # Save the modified image
        image.save('temp_image.png', "PNG")

        # Set the new image as the window background
        self.set_background_image('temp_image.png')

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_pixmap)
        self.resize(scaled_pixmap.width(), scaled_pixmap.height())

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.close_btn = QPushButton('X', self)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.resize(50, 50)
        self.close_btn.move(int(self.width()/2)-25, 500)

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

        # System tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.icon_image_path))
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_menu = QMenu()
        restore_action = self.tray_menu.addAction("Restore")
        quit_action = self.tray_menu.addAction("Quit")
        self.tray_icon.setContextMenu(self.tray_menu)
        restore_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(QApplication.quit)
        self.tray_icon.show()

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

    def update_checkbox_state(self, is_running):
        self.security_checkbox.setChecked(is_running)

    def closeEvent(self, event):
        # Minimize to system tray instead of exiting
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Application Minimized", "Your application is still running.", QIcon(self.icon_image_path))
