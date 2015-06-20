#!/usr/bin/env python
#
# Corey Goldberg, 2015


"""
Process current directory of MP3 & FLAC audio files.

Clear pictures.
Clear all tags and metadata.
Re-tag with 'Artist - Title' from filename.
"""


import glob
import os

from mutagen import File

dry_run = False
start_dir = './test_files/.'



if __name__ == '__main__':
    for root, dirs, files in os.walk(start_dir):
        for filename in files:
            filepath = os.path.abspath(os.path.join(root, filename))
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
                    if not dry_run:
                        audio.save(v1=0, v2_version=3)
                    print(audio.pprint())
                elif 'audio/x-flac' in audio.mime:
                    audio.delete()
                    audio.clear_pictures()
                    audio['artist'] = artist
                    audio['title'] = title
                    if not dry_run:
                        audio.save(deleteid3=True)
                    print(audio.pprint())
                else:
                    print('Invalid Audio File: %r' % filepath)
            print('')
    print('Done.\nProcessed %d files.' % len(files))

