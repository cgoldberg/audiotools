#!/usr/bin/env python3
#
# Corey Goldberg, 2015-2025
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


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def get_artist_title_from_filename(filepath):
    filename = os.path.basename(filepath)
    base = os.path.splitext(filename)[0]
    try:
        artist, title = base.split(" - ", 1)
    except ValueError:
        msg = f"No file name delimiter found: {filepath}"
        logger.error(msg)
        raise ValueError(msg)
    return artist, title


def clear_and_set_tags(audio, artist, title):
    audio.delete()
    audio["artist"] = artist
    audio["title"] = title
    if "audio/x-mp3" in audio.mime:
        audio.save(v1=0, v2_version=3)
    elif "audio/x-flac" in audio.mime:
        audio.clear_pictures()
        audio.save(deleteid3=True)
    else:
        msg = f"Invalid audio file: {filepath}"
        logger.error(msg)
        raise Exception(msg)


def retag(filepath):
    logger.debug(f"Loading File: {filepath}")
    audio = File(filepath, easy=True)
    if audio is None:
        logger.debug(f"Invalid audio file: {filepath}")
    else:
        try:
            artist, title = get_artist_title_from_filename(filepath)
        except ValueError:
            return
        try:
            clear_and_set_tags(audio, artist, title)
        except Exception:
            logger.debug(f"Invalid audio file: {filepath}")
        logger.info("%s - %s" % (artist, title))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="?", default=os.getcwd(), help="start directory")
    args = parser.parse_args()

    count = 0
    for root, dirs, files in os.walk(args.dir):
        for filename in files:
            if filename.endswith((".flac", ".mp3")):
                filepath = os.path.abspath(os.path.join(root, filename))
                retag(filepath)
                count += 1

    logger.info(f"\nDone.\nProcessed {count} audio files.")
