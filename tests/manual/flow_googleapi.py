from google_auth_oauthlib.flow import Flow

# Create the flow using the client secrets file from the Google API
# Console.
flow = Flow.from_client_secrets_file(
    'C:\Python_all_projects\Serious Projects\DuLu\client_secret_970126126184-f6emcrbkk8s7g8hqdva44m4vk882lria.apps.googleusercontent.com.json',
    scopes=['https://www.googleapis.com/auth/youtube.upload'],
    redirect_uri='https//:localhost:8000')

# Tell the user to go to the authorization URL.
auth_url, _ = flow.authorization_url(prompt='consent')

print('Please go to this URL: {}'.format(auth_url))

# The user will get an authorization code. This code is used to get the
# access token.
code = input('Enter the authorization code: ')
flow.fetch_token(code=code)

# You can use flow.credentials, or you can just get a requests session
# using flow.authorized_session.
session = flow.authorized_session()
print(session.get('https://www.googleapis.com/userinfo/v2/me').json())