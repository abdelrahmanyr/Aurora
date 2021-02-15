import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from youtubesearchpython import VideosSearch
import moviepy.editor as mp
import os

#Defining spotify credentials (ignore it)
st = "67587c0f933aa8ab2e59377a14d0d315"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "4d35b62383e543679384be5c9ff3fd6a",
                                                           client_secret = "100c64fa520d4f98969c5b1bfdd92e46",))

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
track_name = track['name']
track_url = str(track['external_urls']['spotify'])
track_album = track['album']['name']
track_artist = track['album']['artists'][0]['name']
album_cover = track['album']['images'][0]['url']

#Now search YouTube for the song with `"track_name - track_artist"` and download it as an MP3 file
result = VideosSearch(f"{track_name} - {track_artist} Audio", limit = 1).result()
link = result['result'][0]['link'] #Now use this one to download the track with pytube

#Your Turn !!!
yt_track = YouTube(link).streams.filter().first()
correct_name = remove(f"{track_name} - {track_artist}", "'\/:*?<>|")
yt_track.download(filename = correct_name)

clip = mp.VideoFileClip(f"{correct_name}.mp4")
clip.audio.write_audiofile(f"{correct_name}.mp3")
clip.close()
os.remove(f"{correct_name}.mp4")

