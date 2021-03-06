#!/usr/bin/env python3
#
# Corey Goldberg, 2015-2018
# MIT License

"""
Tag a library of audio files.

 * Walk directories, clean metadata, and add tags to audio files
 * Supports MP3 and FLAC formats
 * Edits are done in-place
 * Existing metadata and tags are deleted
 * Metadata and tags for Artist and Title are added
 * New tags are taken from the filename (files must be named as expected)

  ** Filenames must be named in the format:
     `ARTIST - TITLE.mp3` or `ARTIST - TITLE.flac`
      That is, they must contain a delimiter (" - ") between Artist and Title,
      and end with a valid extension (".mp3" or ".flac")

Requires:
  * Python 3
  * mutagen (python module)
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
