import argparse
import time
import dropbox_image_uploader
import set_community_icon
import set_community_banner

#create an ubuntu notification
import subprocess

#subprocess.run(["notify-send", "startedstarted", "started"])

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('filepath', help='Path to the image file')
parser.add_argument('-icon', action='store_true', help='Set as icon')
parser.add_argument('-banner', action='store_true', help='Set as banner')
args = parser.parse_args()

#subprocess.run(["notify-send", str(args), "started"])

# Upload the image to Dropbox and get the URL
image_url = dropbox_image_uploader.upload_image(args.filepath)

#subprocess.run(["notify-send", "dropbox", "started"])

# Wait for the image to be uploaded
while not image_url:
    print("Waiting for image to be uploaded...")
    time.sleep(1)

print("Image URL:", image_url)

#make ubuntu notification
subprocess.run(["notify-send", "Successful Upload", "started"])


# Update the community icon or banner based on the argument
if args.icon:
    set_community_icon.update_icon(image_url)
    subprocess.run(["notify-send", "ICON", "started"])
elif args.banner:
    # Assuming you have a similar function for banners
    set_community_banner.update_banner(image_url)