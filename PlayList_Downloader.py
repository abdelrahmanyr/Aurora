import pytube
from pytube import Playlist
import moviepy.editor as mp
from moviepy.editor import *
import os

p = Playlist(input("Enter playlist url: "))
# playlist link is "https://www.youtube.com/playlist?list=PLJjm6SwbZK3l4UvoSd42hFg9PQ9Tl2Rhr"


#print(f'Downloading: {p.title}')
print ("Downloading: "+p.title)


for video in p.videos:
    print (video.title)
    video.streams.first().download()
    mp4_file = (video.title+'.mp4')
    mp3_file = (video.title+'.mp3')
    videoo = VideoFileClip(mp4_file)

    audio = videoo.audio
    audio.write_audiofile(mp3_file)
    
    videoo.close()
    audio.close()
    os.remove(video.title+'.mp4')


    #print (p.title[])

'''
for url in p.video_urls[:4]:
    print (url)
'''
print('Number of videos in playlist: %s' % len(p.video_urls))
#x = (p.video_urls)

