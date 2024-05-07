from googleapiclient.discovery import build

api_key = "AIzaSyD-YsZDAQcI26qHDMrkB_eqMaUAiFHEuok"

youtube = build(
    'youtube',
    'v3',
    developerKey=api_key
)

# Make a request to Youtube API
# request = youtube.channels().list(
#     part='snippet,contentDetails',
#     id='UCHpxOAFY8wM51BJ0NcpK3gQ'
# )

# Get a response from API
# response = request.execute()
# print(response)


# Get a subscriptions of Youtube channel
request = youtube.channels().list(
    part='snippet,contentDetails,status',
    id='UCHpxOAFY8wM51BJ0NcpK3gQ'
)
response = request.execute()
print(response)