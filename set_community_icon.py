import requests
from get_auth import get_auth_token

def update_icon(icon_url):

    auth_token = get_auth_token()

    # New icon URL
    #icon_url = 'YOUR_ICON_URL_HERE'

    # Data to be sent
    data = {
        'community_id': 78581,
        'icon': icon_url,  # Change this to the appropriate key for the icon
        'auth': auth_token  # Include the auth token in the request body
    }

    # Making the PUT request
    response = requests.put('https://lemmy.world/api/v3/community', json=data)

    # Check response
    if response.status_code == 200:
        print("Icon updated successfully!")
    else:
        print("Failed to update icon.")
