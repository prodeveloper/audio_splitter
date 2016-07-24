import sh
import math
import sys
from pydub import AudioSegment


def export_main_files(song,no_parts,split_size_secs,folder_name):
    for i in range(0,no_parts - 1):
        big_slice_time = split_size_secs * (i + 1)
        big_slice_time_milli = big_slice_time * 1000
        big_slice_song = song[:big_slice_time_milli]
        interested_slice = big_slice_song[reverse_split_size_milli:]
        export_file(interested_slice,folder_name,name_file(i))
        print (name_file(i))

def export_last_song(song,last_secs):
    last_secs_milli= last_secs * -1000 #We must pick values in negative for last values
    last_part = song[last_secs_milli:]
    export_file(last_part,folder_name,name_file(no_parts-1))

def export_file(song_slice,folder_name,file_name):
    song_slice.export('{}/{}'.format(folder_name,file_name))

def name_file(sec):
    if sec <10:
        return '0{}Label.mp3'.format(sec) ##Assists in ordering of videos
    return '{}Label.mp3'.format(sec)

def boost_sound(song):
    return song + 5

file_name = sys.argv[1] 
split_size_secs = 180
reverse_split_size_milli = -1000 * split_size_secs
folder_name = file_name.replace('.mp3','')
sh.mkdir(folder_name)
song = AudioSegment.from_mp3(file_name)
song = boost_sound(song)

length_song = song.duration_seconds
no_parts = math.ceil(length_song/split_size_secs)
last_secs = length_song - split_size_secs * (no_parts - 1)  
export_main_files(song,no_parts,split_size_secs,folder_name)
export_last_song(song,last_secs)




