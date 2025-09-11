#!/usr/bin/env python
#
# Corey Goldberg, 2015-2025
# MIT License

"""
Tags a library of MP3 or FLAC audio files.

  * Recursively scans a directory for audio files
  * Edits are done in-place:
    * Existing metadata (tags) and pictures are deleted
    * Metadata tags for Artist and Title are added
  * New tags are taken from the file name
  * Files must be named in the format:
    - "Artist - Title.mp3" or "Artist - Title.flac"
    - File names must contain a delimiter (" - ") between Artist and Title,
      and end with a valid extension (".mp3" or ".flac")

Requires:
  * mutagen (python module)
"""


import argparse
import logging
import os
import pathlib

import mutagen


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def get_artist_and_title_from_filename(filepath):
    root_filename = pathlib.Path(filepath).stem
    if " - " not in root_filename:
        raise Exception(f"No delimiter found: {filepath}")
    artist, title = root_filename.split(" - ", 1)
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
        raise Exception(f"Invalid audio file: {filepath}")


def retag(filepath):
    logger.debug(f"Loading File: {filepath}")
    audio = mutagen.File(filepath, easy=True)
    if audio is None:
        logger.error(f"Invalid audio file: {filepath}")
        return None, None
    try:
        artist, title = get_artist_and_title_from_filename(filepath)
        clear_and_set_tags(audio, artist, title)
    except Exception as e:
        logger.error(e)
        return None, None
    return artist, title


def run(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.lower().endswith((".flac", ".mp3")):
                filepath = os.path.abspath(os.path.join(root, filename))
                artist, title = retag(filepath)
                if None not in (artist, title):
                    logger.info(f"{artist} - {title}")
                    count += 1
    logger.info(f"\nProcessed {count} audio files")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=os.getcwd(), help="start directory")
    args = parser.parse_args()
    run(args.dir)
