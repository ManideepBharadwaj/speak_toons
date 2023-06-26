# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 18:52:01 2023

@author: manideep bhardwaj
"""

import pyaudio
import wave
import assemblyai as aai
from voice_authentication import voice_authentication

from main_functions import *

V = voice_authentication()

class asr(object):
    def __init__(self):
        
        if V.test == False:
            return
        else:
            F=int(input("How many seconds do you want to ask: "))
            if F>15:
                print("Choose a number less than or equal to 15")
                asr()
                return
        
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = F
        FILENAME = "./test.wav"
        
        audio = pyaudio.PyAudio()
        
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        
        print("recording...")
        frames = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        waveFile = wave.open(FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        
        print("finished recording")
    
        aai.settings.api_key = "80753aa91eba47cf84b5e19f72a23177"
        transcriber = aai.Transcriber()
    
        transcript = transcriber.transcribe(FILENAME)
    
        print(transcript.text)
        
        self.text = transcript.text
       
if __name__ == '__main__':
    asr()