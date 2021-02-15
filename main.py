import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import kivy
import pytube

#Defining spotify credentials
st = "67587c0f933aa8ab2e59377a14d0d315"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "4d35b62383e543679384be5c9ff3fd6a",
                                                           client_secret = "100c64fa520d4f98969c5b1bfdd92e46",))

#Giving the track name, album name, artist and album cover
track = input("Type the track URL to search within Youtube")
results_s = sp.search(q={track}, type='track')
items = results_s['tracks']['items']
try:
    track = items[0]
except IndexError:
    print("Sorry I couldn't find any results")
track_name = track['name']
track_url = str(track['external_urls']['spotify'])
track_album = track['album']['name']
track_artist = track['album']['artists'][0]['name']
album_cover = track['album']['images'][0]['url']

#Now search YouTube for the song with `"track_name - track_artist"` and download it as an MP3 file

