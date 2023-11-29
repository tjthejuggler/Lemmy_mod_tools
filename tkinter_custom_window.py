from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QPoint, QSize
import sys

class TransparentWindow(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.initUI(image_path)

    def initUI(self, image_path):
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable window transparency
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window decorations

        # Load and scale the image
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio)  # Adjust size as needed
        label = QLabel(self)
        label.setPixmap(scaled_pixmap)
        self.resize(scaled_pixmap.width(), scaled_pixmap.height())

        # Close Button
        self.close_btn = QPushButton('X', self)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.resize(40, 20)
        self.close_btn.move(self.width() - 50, 10)  # Adjust position as needed

        # Minimize Button
        self.minimize_btn = QPushButton('-', self)
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.minimize_btn.resize(40, 20)
        self.minimize_btn.move(self.width() - 100, 10)  # Adjust position as needed

        self.show()

        self.oldPos = self.pos()

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

def main():
    app = QApplication(sys.argv)
    ex = TransparentWindow('/home/lunkwill/projects/Lemmy_mod_tools/full_ballshead.png')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



