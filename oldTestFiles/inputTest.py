import os

directoryOfFiles = input('enter the directory to audio files to transcribe: ')
directoryListDir = os.listdir(directoryOfFiles)
SUPPORTED_FILE_EXTENSIONS = (".flac")

for file in directoryListDir:
    if(file.endswith(SUPPORTED_FILE_EXTENSIONS)):
        with open(f'{directoryOfFiles}{os.sep}{file}TranscribedAudio.txt', 'w+') as file:
            file.write('hey')
