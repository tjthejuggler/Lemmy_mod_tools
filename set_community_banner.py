import requests
from get_auth import get_auth_token

def update_banner(banner_url):

    auth_token = get_auth_token()

    # New banner URL
    #banner_url = 'https://dl.dropboxusercontent.com/scl/fi/9s2kbsyni3qmky1y2jbfl/ComfyUI_05068_.png?rlkey=qif33jh0c342uc5nvvx6ro5l4&dl=0'

    # Data to be sent
    data = {
        'community_id': 78581,
        'banner': banner_url,
        'auth': auth_token  # Include the auth token in the request body
    }

    # Making the PUT request
    response = requests.put('https://lemmy.world/api/v3/community', json=data)

    # Print the response content for debugging
    #print(response.content)

    # Check response
    if response.status_code == 200:
        print("Banner updated successfully!")
    else:
        print("Failed to update banner.")
