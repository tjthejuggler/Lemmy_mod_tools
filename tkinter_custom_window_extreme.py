from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from Xlib import X, display
from Xlib.ext import composite
from Xlib.protocol import request

class TransparentWindow(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.initUI(image_path)

    def initUI(self, image_path):
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable window transparency
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window decorations

        label = QLabel(self)
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()

        self.make_click_through()

    def make_click_through(self):
        d = display.Display()
        root = d.screen().root
        window_id = int(self.winId())  # Convert sip.voidptr to an integer

        # Your X11 code here...


        # The below X11 interactions are highly experimental and might need to be adjusted
        composite.redirect_window(window_id, composite.RedirectManual)
        win_attrs = root.get_full_property(d.intern_atom('_NET_WM_WINDOW_TYPE'), X.AnyPropertyType).value
        win_attrs = [d.intern_atom('_NET_WM_WINDOW_TYPE_DOCK'), d.intern_atom('_NET_WM_STATE_SKIP_TASKBAR'), d.intern_atom('_NET_WM_STATE_SKIP_PAGER')]
        d.create_window(window_id, 0, 0, self.width(), self.height(), 0, X.CopyFromParent, X.InputOutput, X.CopyFromParent, X.StructureNotifyMask, win_attrs)
        d.sync()

def main():
    app = QApplication(sys.argv)
    ex = TransparentWindow('/home/lunkwill/projects/Lemmy_mod_tools/telegram_bot_icon5.png')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
