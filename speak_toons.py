# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:28:17 2023

@author: manideep bhardwaj
"""

from text_to_speech import text_to_speech
from pydub import AudioSegment
from scipy.io import wavfile
from playsound import playsound
import multiprocessing
import os
import openai

f = text_to_speech()
openai.api_key = os.getenv("OPENAI_API_KEY")
class speak_toons(object):
    def __init__(self):
        filename = 'speech.wav'
        sound = AudioSegment.from_file(filename, format=filename[-3:])
        octaves = 0.3
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        hipitch_sound = hipitch_sound.set_frame_rate(44100)
        hipitch_sound.export("out.wav", format="wav")
        p = multiprocessing.Process(target=playsound, args=("out.wav",))
        p.start()
        input("press ENTER to stop the response")
        p.terminate()
if __name__ == '__main__':
    speak_toons()
        
