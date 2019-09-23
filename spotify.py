import tele
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
scope = 'playlist-modify-public'
username = os.getenv('USERNAME')
redirect_uri = os.getenv('REDIRECT_URI')

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
spotify = spotipy.Spotify(auth=token)

unfound = []            

def user_playlist_get_or_create(username, name):
    all_playlists = spotify.user_playlists(username)
    for playlist in all_playlists['items']:
        if playlist['name'] == name:
            return playlist['id']
    return spotify.user_playlist_create(username, name)['id']


if token:
    playlist_id = user_playlist_get_or_create(username, tele.playlist_name)
    tracks = []
    for song in tele.songs:
        results = spotify.search(q=song, limit=3)['tracks']['items']
        if len(results) > 0:
            first_result = results[0]
            uri, artist, song_name = first_result['uri'], first_result['album']['artists'][0]['name'], first_result['name']
            tracks.append(first_result['uri'])
            # print("Successfully got song" %(artist + ': ' + song_name))
        else:
            unfound.append(song)
            tele.print_red("Failed to get song %s from spotify " %song)
            
    paginate = 0
    while paginate < len(tracks):
        next_page = paginate + 100
        paged_tracks = tracks[paginate:next_page]
        paginate = next_page
        spotify.user_playlist_add_tracks(username, playlist_id, paged_tracks)

tele.save_file(unfound, "failed_spotify")