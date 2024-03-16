import whisper
import os
import torch
import pickle

sep = os.sep
modelSize = "medium"
model = whisper.load_model(modelSize)
options = whisper.DecodingOptions(fp16=torch.cuda.is_available(), language="English")
testFile = "testFile.flac"
transcribedObject = model.transcribe(testFile, fp16=True)
with open('transcribedAui.pickle', 'wb') as pic:
    pickle.dump(transcribedObject, pic)
