import whisper
import os

sep = os.sep
modelSize = "large"
model = whisper.load_model(modelSize)
testFile = "C:Users\icavi\Downloads\craigJan28Recordings\\1-oldirtypanda_0.flac"
text = model.transcribe(testFile).text

with open (f"transcibeTest{modelSize}", 'w') as fileToWrite:
    fileToWrite.write(text)
