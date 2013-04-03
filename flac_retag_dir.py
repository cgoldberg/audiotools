#!/usr/bin/env python
#
# Corey Goldberg, 2013
# Python 2.7


"""
Re-tag a dir of flac files with artist/title meta-data from filenames.

"""


import argparse
import glob
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

    print '  cleared meta-data and tagged flac with:'
    print '  artist: %r' % artist
    print '  title: %r' % title


if __name__ == '__main__':
    flac_files = glob.glob('*.flac')

    for filename in flac_files:
        retag_flac(filename)

    print ''
    print '-' * 16
    print 'done.'
    print 'tagged %d flac files.' % len(flac_files)
