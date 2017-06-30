#!/usr/bin/env python
# Corey Goldberg, 2015
# MIT Licensed

"""
Walk directories, clean and tag audio files.
Supports MP3 and FLAC formats.

Filenames must be in the format: 'Artist - Title.mp3' or 'Artist - Title.flac'.
(spaces, dashes, and multiple words are fine; but must contain " - " to delimit
Artist and Title.  Existing metadata is deleted and new tags (Artist and Title only)
are derived from the filename.
"""

import argparse
import logging
import os

from mutagen import File


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def get_artist_title_from_filename(filepath):
    filename = os.path.basename(filepath)
    pieces = os.path.splitext(filename)
    basename = pieces[0]
    extension = pieces[1]
    if extension.lower() not in ('.flac', '.mp3'):
        msg = 'Invalid File Extension: %r' % extension
        logger.error(msg)
        raise ValueError(msg)
    try:
        artist, title = basename.split(' - ', 1)
    except ValueError:
        msg = 'No File Name Delimiter Found: %r' % filepath
        logger.error(msg)
        raise ValueError(msg)
    return artist, title


def clear_and_set_tags(audio, artist, title):
    audio.delete()
    audio['artist'] = artist
    audio['title'] = title
    if 'audio/x-mp3' in audio.mime:
        audio.save(v1=0, v2_version=3)
    elif 'audio/x-flac' in audio.mime:
        audio.clear_pictures()
        audio.save(deleteid3=True)
    else:
        msg = 'Invalid Audio File: %r' % filepath
        logger.error(msg)
        raise Exception(msg)


def retag(filepath):
    logger.debug('Loading File: %r' % filepath)
    audio = File(filepath, easy=True)
    if audio is None:
        logger.debug('Invalid Audio File: %r' % filepath)
    else:
        try:
            artist, title = get_artist_title_from_filename(filepath)
        except ValueError:
            return
        try:
            clear_and_set_tags(audio, artist, title)
        except Exception:
            logger.debug('Invalid Audio File: %r' % filepath)
        logger.info('%s - %s' % (artist, title))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
                        help='start directory')
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.dir):
        for filename in files:
            filepath = os.path.abspath(os.path.join(root, filename))
            retag(filepath)
    logger.info('\nDone.\nProcessed %d files.' % len(files))

