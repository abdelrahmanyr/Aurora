import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from pytube import Playlist
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

#A funcion for applying metadata to a song
def get_metadata(track, filename):
    album = sp.album(track['album']['id'])
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
    correct_name = remove(filename, "'.\/:*?<>|")
    audiofile = eyed3.load(f"{correct_name}.mp3")
    tag = audiofile.tag
    tag.artist = track_artist
    tag.album = track_album
    tag.title = track_name
    tag.recording_date = eyed3.core.Date(year = int(album_year), month = int(album_month), day = int(album_day))
    tag.track_num = track_number
    tag.disc_num = track_disc_number
    tag.images.set(3, open(album_cover, "rb").read(), "image/jpeg")
    tag.save(version = (2, 3, 0))
    os.remove(f"{track_album}.jpg")

#A function to download a track from Youtube
def download_track(track, dtype, platform : str, track_name = None, track_artist = None):
    if platform == "youtube":
        name = track.title
    elif platform == "spotify":
        query = f"{track_name} - {track_artist} Audio"
        name = f"{track_name} - {track_artist}"
        result = VideosSearch(query, limit = 1).result()
        link = result['result'][0]['link']
    else:
        pass

    if dtype == "ytplaylist":
        yt_track = track.streams.first()
    else:
        yt_track = track.streams.first()
    correct_name = remove(name, "'.\/:*?<>|")
    yt_track.download(filename = correct_name)

    clip = mp.VideoFileClip(f"{correct_name}.mp4")
    audio = clip.audio
    clip.audio.write_audiofile(f"{correct_name}.mp3")
    clip.close()
    audio.close()
    os.remove(f"{correct_name}.mp4")

#The main code
platform = input("What platform your request is on ? (Youtube - Spotify):\n").lower()
#Youtube Condition
if platform == "youtube":
    request_type = input("Please choose between 'Track', 'Playlist':").lower()

    if request_type == "track":
        track_spotify_url = input("Type a Youtube track link to get ID3 tags and album art from (optional):\n")
        track_sp = sp.track(track_spotify_url)
        track = input("Please type a URL for a Youtube video:\n")
        yt_track = YouTube(track).streams.filter().first()
        correct_name = remove(yt_track.title, "'\/:*?<>|")
        download_track(YouTube(track), "yttrack","youtube")
        if not track_spotify_url == "":
            get_metadata(track_sp, f"{correct_name}")

    elif request_type == "playlist":
        playlist = Playlist(input("Please type a URL for a Youtube playlist::\n"))
        for video in playlist.videos:
            download_track(video, "ytplaylist", "youtube")
    else:
        print("Please either type 'track' or 'playlist'")


#Spotify Condition
elif platform == "spotify":
    request_type = input("Please choose between 'Track', 'Playlist', 'Album':").lower()

    if request_type == "track":
        track_id = input("Please type a URL or ID for a Spotify track:\n")
        try:
            track = sp.track(track_id)
        except spotipy.exceptions.SpotifyException:
            print("Sorry I couldn't find any results")
        download_track(track, "strack", "spotify", track['name'], track['artists'][0]['name'])
        get_metadata(track, f"{track['name']} - {track['artists'][0]['name']}")
    elif request_type == "playlist":
        playlist_id = input("Please type a URL or ID for a Spotify playlist:\n")
        try:
            playlist_tracks = sp.playlist_tracks(playlist_id)
        except spotipy.exceptions.SpotifyException:
            print("Sorry I couldn't find any results")
        for track in playlist_tracks['items']:
            track = sp.track(track['track']['id'])
            download_track(track, "splaylist", "spotify", track['name'], track['artists'][0]['name'])
            get_metadata(track, f"{track['name']} - {track['artists'][0]['name']}")

    elif request_type == "album":
        album_id = input("Please type a URL or ID for a Spotify album:\n")
        try:
            album_tracks = sp.album_tracks(album_id)
        except spotipy.exceptions.SpotifyException:
            print("Sorry I couldn't find any results")
        for track in album_tracks['items']:
            track = sp.track(track['id'])
            download_track(track, "splaylist", "spotify", track['name'], track['artists'][0]['name'])
            get_metadata(track, f"{track['name']} - {track['artists'][0]['name']}")
    else:
        print("Please either type 'track' or 'playlist'")

else:
    print("Please either type 'Spotify' or 'Youtube:'")