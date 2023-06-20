import os
import google.auth
import pprint
from googleapiclient.discovery import build
import core.settings as settings


# Set up the YouTube API client
API_KEY = settings.YOUTUBE_API_KEY
youtube = build("youtube", "v3", developerKey=API_KEY)

# Set the ID of the YouTube channel you want to fetch videos from
CHANNEL_ID = settings.CHANNEL_ID

# Define the parameters for the API request
request = youtube.search().list(
    part="id,snippet",
    channelId=CHANNEL_ID,
    maxResults=50,  # You can set the number of videos to fetch
    order="date",
    type="video"
)

# Send the API request and fetch the videos from the channel
response = request.execute()
videos = response.get("items", [])

pprint.pprint(videos)

# Print the title and video ID of each video
for video in videos:
    title = video["snippet"]["title"]
    video_id = video["id"]["videoId"]
    print(f"{title} ({video_id})")
