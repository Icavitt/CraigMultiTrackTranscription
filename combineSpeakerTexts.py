from dataclasses import dataclass
import os
import time

SUPPORTED_FILE_EXTENSIONS = (".txt")

@dataclass
class TranscribedLine:
    timeStampStart: float
    timeStampEnd: float
    lineText: str

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

def removeHallucination(transcribedFile: list[TranscribedLine]) -> list[TranscribedLine]:
    return removeRepeatedSequences(transcribedFile)

def removeRepeatHallucinations(transcribedFile: list[TranscribedLine]) -> list[TranscribedLine]:
    outerIndex = 0
    cloneList = transcribedFile.copy()
    while outerIndex < len(cloneList):
        innerIndex = outerIndex + 1
        while innerIndex < len(cloneList) and cloneList[outerIndex].lineText == cloneList[innerIndex].lineText:
            cloneList.remove(cloneList[innerIndex])
        outerIndex = outerIndex + 1
    return cloneList

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

    

directoryOfFiles = input('enter the directory to audio files to transcribe: ')
directoryListDir = os.listdir(directoryOfFiles)
for file in directoryListDir:
    if(file.endswith(SUPPORTED_FILE_EXTENSIONS)):
        transcribedFile = readFile(f'{directoryOfFiles}{os.sep}{file}')
        cleanedUpFile = removeHallucination(transcribedFile)
        with open(f'{directoryOfFiles}{os.sep}{file[:-4]}CleanedUp.txt', 'w+', encoding='utf-8') as file:
            for line in cleanedUpFile:
                file.write(f'[{line.timeStampStart}, {line.timeStampEnd}] {line.lineText.lstrip()}\n')