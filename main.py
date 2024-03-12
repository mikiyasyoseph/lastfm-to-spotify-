import requests
from datetime import datetime
from config import user, apikey
from pprint import pprint

start_date = datetime(2023, 2, 1)  
end_date = datetime(2023, 2, 28)
from_time = int(start_date.timestamp())
to_time = int(end_date.timestamp())

lastfm_endpoint = f'http://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user={user}&api_key={apikey}&format=json&limit=10&from={from_time}&to={to_time}'
response = requests.get(lastfm_endpoint)
#pprint(response.json())

if response.status_code == 200:
    top_tracks_data = response.json()['weeklytrackchart']
    top_tracks = top_tracks_data['track']
    for track in top_tracks:
        track_name = track['name']
        artist_name = track['artist']['#text']
        play_count = track['playcount']
        print(f"{track_name} by {artist_name} ({play_count} scrobbles)")
else:
    print(f"Failed to fetch top tracks for the specified time period. Status code: {response.status_code}")