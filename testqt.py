import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

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

import change_banner_if_new_post
import change_db_icon
import volume_control
import tb_gui
import tb_telegram

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Test Window')
window.show()
sys.exit(app.exec_())
