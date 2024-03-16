import os
import pickle

object = {}
with open('transcribedAui.pickle', 'rb') as pic:
    object = pickle.load(pic)

with open('transcribeSegmentsTest', 'w') as test:
    for segment in object['segments']:
        test.write(f'[{segment["start"]}, {segment["end"]}] {segment["text"]}\n')