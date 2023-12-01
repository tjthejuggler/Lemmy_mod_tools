import pyautogui
import time

def is_server_running():
    LMstudio_activity_icon = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/Lemmy_mod_tools/LMstudio_activity_icon.png')
    if LMstudio_activity_icon is not None:
        return True
    else:
        return False

def start_server():
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

    time.sleep(2)
    # Locate Start Server button
    start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/Lemmy_mod_tools/LMstudio_activity_icon.png')
    if start_button is not None:
        pyautogui.click(start_button)

    time.sleep(10)

def stop_server():
    
    # Locate Start Server button
    activity_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/Lemmy_mod_tools/LMstudio_activity_icon.png')
    activity_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/Lemmy_mod_tools/LMstudio_activity_icon_light.png')
    if activity_button is not None:
        pyautogui.click(activity_button, button='right')
    elif activity_button is None:
        pyautogui.click(activity_button, button='right')

    time.sleep(2)
    # # Locate Start Server button
    # start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/Lemmy_mod_tools/LMstudio_x.png')
    # if start_button is not None:
    #     pyautogui.click(start_button)

    pyautogui.press('alt')
    pyautogui.press('c')

#stop_server()