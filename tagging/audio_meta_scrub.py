#!/usr/bin/env python
#
# Corey Goldberg, 2015


"""
Walk directories, clean and tag audio files.
Supports MP3 and FLAC formats.

Filenames must be in the format: 'Artist - Title.mp3' or 'Artist - Title.flac'.
(spaces, dashes, and multiple words are fine; but must contain " - " to delimit
Artist and Title.  Existing metadata is deleted and new tags (artist/title only)
are derived from the filename.
"""


import logging
import os

from mutagen import File


start_dir = './test_files/.'


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def retag(filepath):
    logger.info('Loading File: %r' % filepath)
    audio = File(filepath, easy=True)
    if audio is None:
        logger.error('Invalid Audio File: %r' % filepath)
    else:
        basename = os.path.basename(filepath)
        artist, title = os.path.splitext(basename)[0].split(' - ', 1)
        if 'audio/x-mp3' in audio.mime:
            audio.delete()
            audio['artist'] = artist
            audio['title'] = title
            audio.save(v1=0, v2_version=3)
        elif 'audio/x-flac' in audio.mime:
            audio.delete()
            audio.clear_pictures()
            audio['artist'] = artist
            audio['title'] = title
            audio.save(deleteid3=True)
        else:
            logger.error('Invalid Audio File: %r' % filepath)
        logger.info(audio.pprint())


if __name__ == '__main__':
    for root, dirs, files in os.walk(start_dir):
        for filename in files:
            filepath = os.path.abspath(os.path.join(root, filename))
            retag(filepath)
    logger.info('Done.')
    logger.info('Processed %d files.' % len(files))

