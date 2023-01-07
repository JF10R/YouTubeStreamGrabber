import json
import requests
import google.oauth2.credentials

def get_refresh_token():
    # Load the client ID and client secret from the client_secret.json file
    with open('client_secret.json', 'r') as f:
        client_secret = json.load(f)
    CLIENT_ID = client_secret['client_id']
    CLIENT_SECRET = client_secret['client_secret']

    # The scope for the YouTube Data API
    SCOPE = 'https://www.googleapis.com/auth/youtube'

    # The redirect URI for the authorization code grant flow
    REDIRECT_URI = client_secret['redirect_uris'][0]

    # Generate the authorization URL
    authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    authorization_url = f'{authorization_base_url}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}'
    print(f'Please go to the following URL and grant access: {authorization_url}')

    # Prompt the user to visit the authorization URL and grant access
    code = input('Enter the authorization code: ')

    # Exchange the authorization code for an access token and refresh token
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=data)
    token_response = response.json()
    refresh_token = token_response['refresh_token']
    print(refresh_token)
    return refresh_token

get_refresh_token()
