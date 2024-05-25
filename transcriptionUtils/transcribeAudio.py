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

def transcribeAudioFile(fileWithPath: str):
    fileName = f'{fileWithPath}-TranscribedAudio'
    inProgressFileName = f'{fileName}-InProgress.txt'
    completedFileName = f'{fileName}.txt'
    transcribedAudio = MODEL.transcribe(fileWithPath, language="en", fp16=True)
    with open(inProgressFileName, 'w+', encoding='utf-8') as file:
        for segment in transcribedAudio['segments']:
            file.write(f'[{segment["start"]}, {segment["end"]}] {segment["text"]}\n')
    os.rename(inProgressFileName, completedFileName)
    return completedFileName

