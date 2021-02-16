import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from youtubesearchpython import VideosSearch
import moviepy.editor as mp
import os
import eyed3
import requests

#Defining spotify credentials (ignore it)
st = "67587c0f933aa8ab2e59377a14d0d315"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "4d35b62383e543679384be5c9ff3fd6a",
                                                           client_secret = "100c64fa520d4f98969c5b1bfdd92e46"))

#A function for removing illegal characters
def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value;

#Giving the track name, album name, artist and album cover (ignore it too)
track_id = input("Please type a Spotify track URL or ID:\n")
try:
    track = sp.track(track_id)
except spotipy.exceptions.SpotifyException:
    print("Sorry I couldn't find any results")
album = sp.album(track['album']['id'])
pprint.pprint(album)
track_name = track['name']
track_url = str(track['external_urls']['spotify'])
track_album = track['album']['name']
track_artist = track['artists'][0]['name']
track_disc_number = track['disc_number']
track_number = track['track_number']
track_genre_raw = album['genres']
track_genre = (f"{genre}" for genre in track_genre_raw)
album_cover_raw = track['album']['images'][0]['url']
album_type = str(track['album']['type'])
album_artists_raw = track['album']['artists']
album_artists = (f"{artist['name']}" for artist in album_artists_raw)
album_year, album_month, album_day = track['album']['release_date'].split("-")
album_total_tracks = track['album']['total_tracks']

response = requests.get(album_cover_raw)

file = open(f"{track_album}.jpg", "wb")
file.write(response.content)
file.close()
album_cover = f"{track_album}.jpg"

#Now search YouTube for the song with `"track_name - track_artist"` and download it as an MP3 file
result = VideosSearch(f"{track_name} - {track_artist} Audio", limit = 1).result()
link = result['result'][0]['link'] #Now use this one to download the track with pytube

#Your Turn !!!
yt_track = YouTube(link).streams.filter().first()
correct_name = remove(f"{track_name} - {track_artist}", "'\/:*?<>|")
yt_track.download(filename = correct_name)

clip = mp.VideoFileClip(f"{correct_name}.mp4")
audio = clip.audio
clip.audio.write_audiofile(f"{correct_name}.mp3")
clip.close()
audio.close()
os.remove(f"{correct_name}.mp4")

#Now changing the song metadata
audiofile = eyed3.load(f"{correct_name}.mp3")
tag = audiofile.tag
tag.artist = track_artist
tag.album = track_album
tag.album_artist = album_artists
tag.title = track_name
tag.recording_date = eyed3.core.Date(year = int(album_year), month = int(album_month), day = int(album_day))
tag.track_num = track_number
tag.disc_num = track_disc_number
tag.images.set(3, open(album_cover, "rb").read(), "image/jpeg")
tag.save(version = (2, 3, 0))
os.remove(f"{track_album}.jpg")