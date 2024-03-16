from dataclasses import dataclass
import os
import time
import copy

SUPPORTED_FILE_EXTENSIONS = (".txt")

@dataclass
class TranscribedLine:
    timeStampStart: float
    timeStampEnd: float
    lineText: str

@dataclass
class TranscibedLineWithSpeaker(TranscribedLine):
    speaker: str

@dataclass
class SpeakerAndLines:
    speaker: str
    lines: list[TranscribedLine]

def readFile(pathToFile) -> list[TranscribedLine]:
    arrLinesAndTimes =[]
    with open(f'{pathToFile}', 'r', encoding='utf-8') as file:
        while line := file.readline():
            arrLinesAndTimes.append(extractLineComponents(line))
    return arrLinesAndTimes

def extractLineComponents(line) -> TranscribedLine:
    timeStampAndLineText = line[1:].split(']')
    startTimeEndTime = timeStampAndLineText[0].split(',')
    startTime = startTimeEndTime[0].strip()
    endTime = startTimeEndTime[1].strip()
    lineText = timeStampAndLineText[1].strip()
    return TranscribedLine(float(startTime), float(endTime), lineText)

def processWhisperTranscribedAudio(transcribedFile: list[TranscribedLine]) -> list[TranscribedLine]:
    dehallucinatedFile = removeRepeatedSequences(transcribedFile)
    return dehallucinatedFile
    # return combineContiguousAudio(dehallucinatedFile)

def removeRepeatHallucinations(transcribedFile: list[TranscribedLine]) -> list[TranscribedLine]:
    outerIndex = 0
    cloneList = transcribedFile.copy()
    while outerIndex < len(cloneList):
        innerIndex = outerIndex + 1
        while innerIndex < len(cloneList) and cloneList[outerIndex].lineText == cloneList[innerIndex].lineText:
            cloneList.remove(cloneList[innerIndex])
        outerIndex = outerIndex + 1
    return cloneList

# Playing with how it reads to have multiple lines of audio transcribed together
# def combineContiguousAudio(transcribedFile: list[TranscribedLine]) -> list[TranscribedLine]:
#     i = 0
#     cloneList = copy.deepcopy(transcribedFile)
#     while i < len(cloneList)-1:
#         currLine = cloneList[i]
#         nextLine = cloneList[i+1]
#         while currLine.timeStampEnd == nextLine.timeStampStart:
#             currLine.lineText = f'{currLine.lineText} {nextLine.lineText}'
#             currLine.timeStampEnd = nextLine.timeStampEnd
#             del cloneList[i+1:i+2]
#         i = i +1
#     return cloneList

# This function removes repated sequences of tnrascribed lines
# This is another type of hallucination that occurs and causes repeat junk text
# These repeated sequences are always adjacent
def removeRepeatedSequences(transcribedFile: list[TranscribedLine]) -> list[TranscribedLine]:
    cloneList = transcribedFile.copy()
    maxSequenceLength = 10
    outerIndex = 0
    while outerIndex < len(cloneList):
        compareSeqIndex = outerIndex
        sequence = []
        sequenceOffset = 1
        sequencesDeleted = False
        while len(sequence) < maxSequenceLength and outerIndex + sequenceOffset < len(cloneList) and not sequencesDeleted:
            compareSeqIndex = outerIndex + sequenceOffset
            while compareSeqIndex + sequenceOffset <= len(cloneList) and sequencesAreSame(cloneList[outerIndex:outerIndex+sequenceOffset], cloneList[compareSeqIndex:compareSeqIndex+sequenceOffset]):
                print(f'removing indices {compareSeqIndex} to {compareSeqIndex+sequenceOffset}')
                del cloneList[compareSeqIndex:compareSeqIndex+sequenceOffset]
                sequencesDeleted = True
            sequenceOffset = sequenceOffset + 1
        outerIndex = outerIndex+1
    return cloneList

def sequencesAreSame(baseSequence: list[TranscribedLine], comparedToSequnece:list[TranscribedLine]) -> bool:
    for baseLine, comparedToline in zip(baseSequence, comparedToSequnece):
        if(baseLine.lineText != comparedToline.lineText): return False
    return True

#won't support 10+ channels
def getSpeaker(fileName: str) -> str:
    endIndex = fileName.find('.flac')
    return fileName[2:endIndex]

def preprocessFiles(path: str, files: list[str]) -> dict[str, list[TranscribedLine]]:
    allFiles = {}
    for file in files:
        if(file.endswith(SUPPORTED_FILE_EXTENSIONS)):
            transcribedFile = readFile(f'{path}{os.sep}{file}')
            cleanedUpFile = processWhisperTranscribedAudio(transcribedFile)
            speaker = getSpeaker(file)
            allFiles[speaker] = cleanedUpFile
    return allFiles

def combineSpeakers(speakerLines: dict[str, list[TranscribedLine]]) -> list[TranscibedLineWithSpeaker]:
    indices = {speaker: 0 for speaker in speakerLines}
    allLines = []
    iterableIndices = [speaker for speaker, lines in speakerLines if indices[speaker] < len(lines)]
    mapped = map(lambda speaker: (speaker, speakerLines[speaker][indices[speaker]]), iterableIndices)
    indexToIter = sorted(mapped, key=lambda speakerTranscribedLineTuple: speakerTranscribedLineTuple[1].timeStampStart)[0]
    while len(iterableIndices) > 0:
        speaker = indexToIter[0]
        line = indexToIter[1]
        allLines.append(TranscibedLineWithSpeaker(speaker=speaker, timeStampStart=line.timeStampStart, timeStampEnd=line.timeStampEnd, lineText=line.lineText))
        indices[indexToIter[0]] =  indices[indexToIter[0]] + 1
    return allLines

directoryOfFiles = input('enter the directory to audio files to transcribe: ')
directoryListDir = os.listdir(directoryOfFiles)
preProcessedFiles = preprocessFiles(directoryOfFiles, directoryListDir)
combineSpeakers(preProcessedFiles)
for file in directoryListDir:
    if(file.endswith(SUPPORTED_FILE_EXTENSIONS)):
        transcribedFile = readFile(f'{directoryOfFiles}{os.sep}{file}')
        cleanedUpFile = processWhisperTranscribedAudio(transcribedFile)
        with open(f'{directoryOfFiles}{os.sep}{file[:-4]}CleanedUp.txt', 'w+', encoding='utf-8') as file:
            for line in cleanedUpFile:
                file.write(f'[{line.timeStampStart}, {line.timeStampEnd}] {line.lineText.lstrip()}\n')