import requests
from datetime import datetime
import config

start_date = datetime(2024, 2, 1)  # Start date (YYYY, MM, DD)
end_date = datetime(2024, 2, 29)  # End date (YYYY, MM, DD)
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')
 
lastfm_endpoint = f'http://ws.audioscrobbler.com/2.0/?method=user.getTopTracks&user={user}&api_key={apikey}&format=json&date={start_date_str},{end_date_str}&limit=50'

response = requests.get(lastfm_endpoint)

top_tracks_data = response.json()['toptracks']
top_tracks = top_tracks_data['track']

for track in top_tracks:
    track_name = track['name']
    artist_name = track['artist']['name']
    play_count = track['playcount']
    print(f"{track_name} by {artist_name} (Played {play_count} times)")