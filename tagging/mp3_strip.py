#!/usr/bin/env python
#
# Corey Goldberg, 2013


"""
Remove all ID3 and APE tags from an MP3 audio file.

This script takes one commandline argument: an MP3 filename.
It will clear any existing metadata/tags.
"""


import argparse

import mutagen
import mutagen.mp3
import mutagen.apev2


def strip_tags(filename):
    print('processing: %r' % filename)

    f = mutagen.File(filename)

    try:
        f.load(filename, ID3=mutagen.mp3.MP3)
        f.delete()
        f.save()
    except ValueError:
        pass

    try:
        f.load(filename, ID3=mutagen.apev2.APEv2)
        f.delete()
        f.save()
    except ValueError:
        pass

    print('cleared meta-data.')
    print('done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='MP3 file name')
    args = parser.parse_args()
    strip_tags(args.filename)
