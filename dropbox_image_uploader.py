import dropbox
import requests
import json
import time

# Dropbox app credentials
with open('/home/lunkwill/projects/Lemmy_mod_tools/dropbox_app_key.txt', 'r') as f:
    APP_KEY = f.read().strip()

with open('/home/lunkwill/projects/Lemmy_mod_tools/dropbox_app_secret.txt', 'r') as f:
    APP_SECRET = f.read().strip()



# Dropbox access token
with open('/home/lunkwill/projects/Lemmy_mod_tools/dropbox_access_token.txt', 'r') as f:
    access_token = f.read()

# Function to refresh access token
def refresh_access_token(refresh_token):
    token_url = "https://api.dropbox.com/oauth2/token"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(token_url, data=data, auth=(APP_KEY, APP_SECRET))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Failed to refresh token")

# Function to upload image
def upload_image(file_path):
    # Read refresh token from file
    with open('/home/lunkwill/projects/Lemmy_mod_tools/dropbox_refresh_token.txt', 'r') as f:
        refresh_token = f.read().strip()

    # Try to use the existing access token, refresh if expired
    try:
        with open('/home/lunkwill/projects/Lemmy_mod_tools/dropbox_access_token.txt', 'r') as f:
            access_token = f.read().strip()

        dbx = dropbox.Dropbox(access_token)
        # Test if token is valid by making a simple API call
        dbx.users_get_current_account()
    except dropbox.exceptions.AuthError:
        # Refresh token if there's an authentication error
        access_token = refresh_access_token(refresh_token)
        with open('/home/lunkwill/projects/Lemmy_mod_tools/dropbox_access_token.txt', 'w') as f:
            f.write(access_token)
        dbx = dropbox.Dropbox(access_token)

    # Rest of your upload code remains the same...


    # Path to your local image
    #file_path = '/home/lunkwill/Downloads/ComfyUI_05068_.png'

    # Path in your Dropbox
    dropbox_path = file_path.replace('/home/lunkwill/projects/ComfyUI/output/', '/')

    print("Uploading image...", file_path, dropbox_path)

    # Upload the file
    with open(file_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_path)

    # Create a shared link with public settings
    settings = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
    link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path, settings=settings)

    # Get a direct link to the file
    direct_link = link_metadata.url.replace('www.dropbox.com', 'dl.dropboxusercontent.com').replace("?dl=0", "")

    print("Direct Link:", direct_link)

    return direct_link

# upload_image('/home/lunkwill/projects/ComfyUI/output/The_Distress_Context_of_Social_Calls_Evokes_a_Fear_Response_in_the_Bat_Pipistrel_00006_.png')