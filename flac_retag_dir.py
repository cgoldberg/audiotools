#!/usr/bin/env python
#
# Corey Goldberg, 2013
# Python 2.7


"""
Re-tag a directory of flac files with artist/title meta-data from filenames.

This script takes one commandline argument: a directory name of flac
files to re-tag.  The filenames must be in the format:
"Artist - Title.flac".  (spaces, dashes, and multiple words are fine;
but must contain ' - ' to delimit Artist and Title.  It will clear any
existing metadata and write new tags (artist/title only) taken from
the filenames.
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
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', 
        default=os.getcwd(), help='directory name')
    args = parser.parse_args()
    
    flac_files = glob.glob(os.path.join(args.dir, '*.flac'))
    
    for filename in flac_files:
        retag_flac(filename)
    print ''
    print '-' * 16
    print 'done.'
    print 'tagged %d flac files.' % len(flac_files)
