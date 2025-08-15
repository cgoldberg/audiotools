#!/usr/bin/env python
# Corey Goldberg 2013

"""Generate a Spectrogram image for a given audio sample.

Compatible with several audio formats: wav, flac, mp3, etc.
Requires: https://code.google.com/p/timeside/

A spectrogram, or sonogram, is a visual representation of the spectrum
of frequencies in a sound.  Horizontal axis represents time, Vertical axis
represents frequency, and color represents amplitude.
"""


import timeside


audio_file = "sample.wav"

decoder = timeside.decoder.FileDecoder(audio_file)
grapher = timeside.grapher.Spectrogram(width=1920, height=1080)
(decoder | grapher).run()
grapher.render("spectrogram.png")
