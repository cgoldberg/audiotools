#!/usr/bin/env python
#
# Corey Goldberg, 2013


"""
Re-tag flac files with artist/title meta-data from filename.

This script takes one commandline argument: a flac filename to re-tag.
The filename must be in the format: "Artist - Title.flac".  (spaces,
dashes, and multiple words are fine; but must contain ' - ' to delimit
Artist and Title.  It will clear any existing metadata and write
new tags (artist/title only) taken from the filename.
"""


import argparse
import os

from mutagen.flac import FLAC


def retag_flac(filename):
    audio = FLAC(filename)
    audio.delete()
    artist, title = os.path.splitext(filename)[0].split(' - ', 1)
    audio['artist'] = artist
    audio['title'] = title
    audio.save(deleteid3=True)

    print('Cleared metadata and tagged flac with:')
    print('  artist: %r' % artist)
    print('  title: %r' % title)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='flac file name')
    args = parser.parse_args()
    print('File: %r...' % args.filename)
    retag_flac(args.filename)
    print('Done.')