#!/usr/bin/env python
#
# Corey Goldberg, 2015


"""
Walk directories, clean and tag audio files.
Supports MP3 and FLAC formats.

Filenames must be in the format: 'Artist - Title.mp3' or 'Artist - Title.flac'.
(spaces, dashes, and multiple words are fine; but must contain " - " to delimit
Artist and Title.  Existing metadata is deleted and new tags (artist/title only)
are derived from the filename.
"""


import os

from mutagen import File


start_dir = './test_files/.'



def retag(filepath):
    print('Loading File: %r' % filepath)
    audio = File(filepath, easy=True)
    if audio is None:
        print('Invalid Audio File: %r' % filepath)
    else:
        artist, title = os.path.splitext(filename)[0].split(' - ', 1)
        if 'audio/x-mp3' in audio.mime:
            audio.delete()
            audio['artist'] = artist
            audio['title'] = title
            audio.save(v1=0, v2_version=3)
        elif 'audio/x-flac' in audio.mime:
            audio.delete()
            audio.clear_pictures()
            audio['artist'] = artist
            audio['title'] = title
            audio.save(deleteid3=True)
        else:
            print('Invalid Audio File: %r' % filepath)
        print(audio.pprint())
    print('')


if __name__ == '__main__':
    for root, dirs, files in os.walk(start_dir):
        for filename in files:
            filepath = os.path.abspath(os.path.join(root, filename))
            retag(filepath)
    print('Done.\nProcessed %d files.' % len(files))

