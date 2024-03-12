import time, spotipy, requests
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
from config import spotify_client_id, spotify_client_secret, user_id, user, apikey
from datetime import datetime

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'YOUR_SECRET_KEY'
TOKEN_INFO = 'token_info'


start_date = datetime(2023, 2, 1)  
end_date = datetime(2023, 2, 28)
from_time = int(start_date.timestamp())
to_time = int(end_date.timestamp())
lastfm_endpoint = f'http://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user={user}&api_key={apikey}&format=json&limit=10&from={from_time}&to={to_time}'
response = requests.get(lastfm_endpoint)
top_tracks_data = response.json()['weeklytrackchart']
top_tracks = top_tracks_data['track']

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
  
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('create_playlist',_external=True))

@app.route('/createPlaylist')
def create_playlist():
    try: 
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    track_uris = []
    for track in top_tracks:
        track_name = track['name']
        artist_name = track['artist']['#text']
        query = f'remaster%20track:{track_name}%20artist:{artist_name}'
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
    print(track_uris)
    playlist = sp.user_playlist_create(user_id, 'Test')
    playlist_id = playlist['id']
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=track_uris)
    print(f"Playlist created successfully with ID: {playlist_id}")
    return playlist_id

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external=False))
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = spotify_client_id,
        client_secret = spotify_client_secret,
        redirect_uri = 'http://localhost:5000/redirect',
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

app.run(debug=True)