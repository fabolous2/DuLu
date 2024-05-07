import json

from googleapiclient.discovery import build

'''
!!!! Usefull links !!!!! 
https://github.com/googleapis/google-api-python-client
https://github.com/youtube/api-samples
https://developers.google.com/youtube/v3/docs
https://developers.google.com/youtube/v3/determine_quota_cost
 
pip install --upgrade google-api-python-client
 
https://github.com/googleapis/google-cloud-python
'''

API_KEY = 'AIzaSyD-YsZDAQcI26qHDMrkB_eqMaUAiFHEuok'

'''
GET YT API service w API Key only
'''
def get_service():
    service = build('youtube', 'v3', developerKey=API_KEY)
    return service

'''
Get Channel Info(title, desc, stats)
https://developers.google.com/youtube/v3/docs/channels/list
 
Type og Channels Urls
https://www.youtube.com/channel/UCXlhVxzpYqr2WguSWbzRNMw
https://www.youtube.com/c/tntonlineru
https://www.youtube.com/user/tn4east
but my script works only w channel_id (hash)
or w user/tn4east -> replace id=channel_id to forUsername='username'
'''
def get_channel_info(channel_id = ''):
    response = get_service().channels().list(id=channel_id, part='snippet,statistics').execute()

    print(response['items'][0]['smippet'['title']])
    print(response['items'][0]['smippet'['publishedAt']])
    print(response['items'][0]['smippet'['viewCount']])


'''
Get Video Info (title, desc, stats)
https://developers.google.com/youtube/v3/docs/videos/list
'''
def get_video_info(video_id = 'yPun8Xwi5aQ'):
    response = get_service().videos().list(id=video_id, part='snippet,statistics').execute()
    print(json.dumps(response))
    # print(response['items'][1]['snippet']['title'])
    # print(response['items'][1]['statistics']['viewCount'])


if __name__ == '__main__':
    get_video_info('yPun8Xwi5aQ')