import cv2
import time
from pyrogram import Client

def is_motion_detected(reference_frame, current_frame, threshold):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between the current frame and reference frame
    frame_diff = cv2.absdiff(gray1, gray2)

    # Threshold the difference to get the regions with significant changes
    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    # Find the percentage of changed area
    non_zero_pixels = cv2.countNonZero(thresh)
    changed_area = (non_zero_pixels * 100) / (thresh.shape[0] * thresh.shape[1])
    print('changed_area', changed_area)
    # If the changed area exceeds our threshold, motion is detected
    return changed_area > threshold

app = Client("my_account")

# Function to send the image
async def send_image(image_path):
    async with app:
        await app.send_message("lunkstealth_bot", "Motion Detected!")
        await app.send_photo("lunkstealth_bot", image_path)

# Setup webcam
cap = cv2.VideoCapture(0)
ret, previous_frame = cap.read()

while True:
    ret, current_frame = cap.read()
    if ret:
        cv2.imwrite('/home/lunkwill/projects/Lemmy_mod_tools/images/current_image.jpg', current_frame)
        
        if is_motion_detected(previous_frame, current_frame, 0.7):
            print('Motion detected!')
            app.run(send_image('/home/lunkwill/projects/Lemmy_mod_tools/images/current_image.jpg'))

        previous_frame = current_frame

    time.sleep(5)

cap.release()
