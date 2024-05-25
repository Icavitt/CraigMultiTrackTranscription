import os
import transcriptionUtils.transcribeAudio as transcribe
import transcriptionUtils.combineSpeakerTexts as combineSpeakers
SUPPORTED_FILE_EXTENSIONS = (".flac")


def transcribeFilesInDirectory(directoryPath: str):
    filesTranscribed = []
    directoryListDir = os.listdir(directoryPath)
    for file in directoryListDir:
        if(file.endswith(SUPPORTED_FILE_EXTENSIONS)):
            fileNameWithPath = f'{directoryPath}{os.sep}{file}'
            filesTranscribed.append(transcribe.transcribeAudioFile(fileNameWithPath))
        else:
            print(f'Skipping {file} as it\'s not a supported type')
            print(f'supported types are {SUPPORTED_FILE_EXTENSIONS}')
    return filesTranscribed

directoryOfFiles = input('enter the directory to audio files to transcribe: ')
transcribedSpeakerFiles = transcribeFilesInDirectory(directoryOfFiles)
combineSpeakers.combineTranscribedSpeakerFiles(directoryOfFiles)


