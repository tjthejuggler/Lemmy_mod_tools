import pyautogui
import time

time.sleep(2)
start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/Lemmy_mod_tools/LMstudio_icon.png')
if start_button is not None:
    pyautogui.click(start_button)
time.sleep(10)

start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/Lemmy_mod_tools/LMstudio_server_tab.png')
if start_button is not None:
    pyautogui.click(start_button)

time.sleep(2)
# Locate Start Server button
start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/Lemmy_mod_tools/LMstudio_start_server_button.png')
if start_button is not None:
    pyautogui.click(start_button)