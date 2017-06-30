#!/usr/bin/env python3
# Corey Goldberg, 2017
# MIT License

"""
Clean and tag audio files.
Supports MP3 and FLAC formats.

Filenames must be in the format: 'Artist - Title.mp3' or 'Artist - Title.flac'.
(spaces, dashes, and multiple words are fine; but must contain " - " to delimit
Artist and Title.  Existing metadata is deleted and new tags (Artist and Title only)
are derived from the filename.
"""

import argparse
import logging
import os

import taglib


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def parse_filename(filepath):
    if not filepath.endswith(('.flac', '.mp3')):
        logger.error('Invalid File Extension')
        raise SystemExit
    filename = os.path.basename(filepath)
    basename = os.path.splitext(filename)[0]
    try:
        artist, title = basename.split(' - ', 1)
    except ValueError:
        logger.error('No File Name Delimiter Found')
        raise SystemExit
    return artist, title


def tag(filepath):
    logger.info('Loading File: {}'.format(filepath))
    audio = taglib.File(filepath)
    artist, title = parse_filename(filepath)
    audio.tags = {'ARTIST': [artist], 'TITLE': [title]}
    audio.save()
    logger.info('Tagged: {} - {}'.format(artist, title))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
                        help='start directory')
    args = parser.parse_args()
    for filename in os.listdir(args.dir):
        filepath = os.path.abspath(os.path.join(args.dir, filename))
        tag(filepath)
    logger.info('Done')
