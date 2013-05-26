#!/usr/bin/env python
#
# Corey Goldberg, 2013


"""
Process current directory of FLAC audio files.

Clear pictures.
Clear all tags and metadata.
Re-tag with artist/title from filename.
"""


import glob
import os

from mutagen.flac import FLAC


def retag(filename):
    audio = FLAC(filename)
    audio.delete()
    artist, title = os.path.splitext(filename)[0].split(' - ', 1)
    audio['artist'] = artist
    audio['title'] = title
    audio.save(deleteid3=True)
    print('  Cleared metadata.\n  Tagged flac with:')
    print('    artist: %r' % artist)
    print('    title: %r' % title)


def clear_pictures(filename):
    audio = FLAC(filename)
    audio.clear_pictures()
    audio.save()
    print('  Cleared pictures.')


if __name__ == '__main__':
    flac_files = glob.glob('*.flac')

    for filename in flac_files:
        print('File: %r' % filename)
        clear_pictures(filename)
        retag(filename)

    print('Done.')
    print('Processed %d flac files.' % len(flac_files))
