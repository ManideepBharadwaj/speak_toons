# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 18:16:34 2023

@author: manideep bhardwaj
"""

import pyaudio
import wave
import os
import pickle
import time
from scipy.io.wavfile import read
from IPython.display import Audio, clear_output

from main_functions import *

class voice_authentication(object):
    def __init__(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 4
        FILENAME = "./test.wav"
        
        audio = pyaudio.PyAudio()
        
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        
        time.sleep(2.0)
        print("recording...")
        frames = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        waveFile = wave.open(FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        
        modelpath = "./gmm_models/"
        
        gmm_files = [os.path.join(modelpath,fname) for fname in 
                    os.listdir(modelpath) if fname.endswith('.gmm')]
    
        models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
    
        speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]
        
        if len(models) == 0:
            print("No Users in the Database!")
            return
        
        sr,audio = read(FILENAME)
        
        vector = extract_features(audio,sr)
        log_likelihood = np.zeros(len(models))
        
        for i in range(len(models)):
            gmm = models[i]         
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()
    
        pred = np.argmax(log_likelihood)
        identity = speakers[pred]
        
        if identity == 'unknown':
                print("Not Recognized! Try again...")
                return
            
        print( "Recognized as - ", identity)
        
        print("Hi ", identity)
        
        self.test = True
    
if __name__ == '__main__':
    voice_authentication()