# from google.oauth2 import service_account
#
# credentials = service_account.Credentials.from_service_account_file(
#     'C:\\Python_all_projects\\Serious Projects\\DuLu\\auto-poster-test-e9b9315edac0.json'
# )
#
# scoped_credentials = credentials.with_scopes(
#     ['https://www.googleapis.com/auth/youtube.upload']
# )
#

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

flow = InstalledAppFlow.from_client_secrets_file(
    'C:\Python_all_projects\Serious Projects\DuLu\client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.upload'],
    redirect_uri='http://localhost:8000'
)

flow.run_local_server()
credentials = flow.credentials

service = build('youtube', 'v3', credentials=credentials)

# Optionally, view the email address of the authenticated user.
user_info_service = build('oauth2', 'v2', credentials=credentials)
user_info = user_info_service.userinfo().get().execute()
print(user_info)
print(user_info['email'])
