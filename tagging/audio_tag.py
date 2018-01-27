#!/usr/bin/env python3
# Corey Goldberg, 2017, 2018
# MIT License

"""
Clean and tag a directory of audio files.

This program processes a directory of MP3/FLAC audio files.
It deletes existing metadata tags each track with an
Artist and Title derived from the file's name.

Files must be named in the format:
`ARTIST - TITLE.mp3` or `ARTIST - TITLE.flac`
That is, they must contain " - " to delimit artist and title,
and end with a valid extension (".mp3" or ".flac").

Requires:
  * TagLib (audio metadata C++ library)
  * pytaglib (python bindings for TagLib)

"""

import argparse
import logging
import os
import sys

import taglib


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def get_tags_from_filename(filepath):
    basename = os.path.splitext(os.path.basename(filepath))[0]
    try:
        artist, title = basename.split(' - ', 1)
    except ValueError:
        logger.error('No valid delimiter found in filename')
        sys.exit(1)
    return artist, title


def tag(filepath, artist, title):
    new_tags = {'ARTIST': [artist], 'TITLE': [title]}
    audio = taglib.File(filepath)
    audio.tags = new_tags
    audio.removeUnsupportedProperties(audio.unsupported)
    audio.save()
    audio.close()
    logger.info('Tagged: {} - {}'.format(artist, title))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
                        help='working directory')
    args = parser.parse_args()
    for filename in os.listdir(args.dir):
        if filename.endswith(('.flac', '.mp3')):
            filepath = os.path.abspath(os.path.join(args.dir, filename))
            artist, title = get_tags_from_filename(filepath)
            tag(filepath, artist, title)
