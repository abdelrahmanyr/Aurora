from pytube import YouTube
import moviepy.editor as mp
from moviepy.editor import *
import os
yt = YouTube (input ("Enter playlist url: "))

yt.streams.all()

stream = yt.streams.first()

print (stream)

stream.download()

print (yt.title)

mp4_file = (yt.title+'.mp4')
mp3_file = (yt.title+'.mp3')

video = VideoFileClip(mp4_file)
audio = video.audio
audio.write_audiofile(mp3_file)

video.close()
audio.close()

os.remove(yt.title+'.mp4')


