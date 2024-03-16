import whisper
import torch
import sys
import os

MODEL_SIZE = "medium"
MODEL = whisper.load_model(MODEL_SIZE)
if torch.cuda.is_available(): print('CUDA is available, using fp16')
else: 
    print('CUDA not available ending process, update dependencies to fix')
    sys.exit()
SUPPORTED_FILE_EXTENSIONS = (".flac")

directoryOfFiles = input('enter the directory to audio files to transcribe: ')
directoryListDir = os.listdir(directoryOfFiles)
for file in directoryListDir:
    if(file.endswith(SUPPORTED_FILE_EXTENSIONS)):
        transcribedAudio = MODEL.transcribe(f'{directoryOfFiles}{os.sep}{file}', language="en", fp16=True)
        with open(f'{directoryOfFiles}{os.sep}{file}TranscribedAudio.txt', 'w+', encoding='utf-8') as file:
            for segment in transcribedAudio['segments']:
                file.write(f'[{segment["start"]}, {segment["end"]}] {segment["text"]}\n')
