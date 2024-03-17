## Summary
This is a series of scripts utilizing Whisper AI to transcribe multi-channel discord audio. I was using Craig for discord transcription and downloading multi-track .flac files.

There will need to be some modifications for single track files and there won't be any speaker identification.

## Setup
Requires at least python 3.11, and pytorch libraries. Be sure to install CUDA supported libraries if your graphics card supports CUDA.

## Current Use
run `python transcribeWithInputs.py` when prompted pass the absolute path to the directory of audio files to transcribe. Then run `python combineSpeakerTexts.py` and pass the same path. Ensure any audio files or text files that you don't want included in transcription aren't in the folder.