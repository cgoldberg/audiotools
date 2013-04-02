#!/usr/bin/env python
#
# Corey Goldberg, 2013
# Python 2.7


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
    print '\nprocessing: %r...' % filename

    audio = FLAC(filename)
    audio.clear()
    artist, title = os.path.splitext(filename)[0].split(' - ', 1)
    audio['artist'] = artist
    audio['title'] = title
    audio.save()

    print 'cleared meta-data and tagged flac with:'
    print '  artist: %r' % artist
    print '  title: %r' % title
    print 'done.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='flac file name')
    args = parser.parse_args()
    retag_flac(args.filename)
