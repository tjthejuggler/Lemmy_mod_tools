import requests

def get_auth_token():
    auth_token = "None"
    # Your Lemmy credentials
    with open('/home/lunkwill/projects/Lemmy_mod_tools/secrets/username.txt', 'r') as f:
        username = f.read()

    with open('/home/lunkwill/projects/Lemmy_mod_tools/secrets/password.txt', 'r') as f:
        password = f.read()

    # Login data
    login_data = {
        'username_or_email': username,
        'password': password
    }

    # Login request
    response = requests.post('https://lemmy.world/api/v3/user/login', json=login_data)

    # Extracting the auth token
    if response.status_code == 200:
        auth_token = response.json().get('jwt')
        print("Auth Token:", auth_token)
    else:
        print("Failed to log in.")
    return auth_token