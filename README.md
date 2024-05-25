## Summary
This is a small script utilizing Whipser AI to transcribe multi-channel discord audio output from [Craig](https://craig.chat/)

## Setup
Requires at least python 3.11, and pytorch libraries. Be sure to install CUDA supported libraries if your graphics card supports CUDA.

## Current Use
run `python transcribeCraigAudio.py` when prompted pass the absolute path to the directory of audio files to transcribe. After it runs, you'll find in that folder the transcribed audio of each individual speaker - denoted `userName.flac-TranscribedAudio.txt` - and a file with all speakers audio in it - denoted `<directoryName>AllAudio.txt`