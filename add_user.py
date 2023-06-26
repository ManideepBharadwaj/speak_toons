# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 18:30:08 2023

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

if os.path.exists('./voice_database'):
    pass
else:
    os.mkdir("./voice_database")

def add_user():
    
    name = input("Enter Name:")
    
    if os.path.exists('./voice_database/embeddings.pickle'):
        with open('./voice_database/embeddings.pickle', 'rb') as database:
            db = pickle.load(database)
            if name in db or name == 'unknown':
                print("Name Already Exists! Try Another Name...")
                return
            else:
                db = {}
                
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3
    
    source = "./voice_database/" + name
    
    os.mkdir(source)

    for i in range(3):
        audio = pyaudio.PyAudio()

        if i == 0:
            time.sleep(2.0)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Speak I am {} on 3 seconds ".format(name))
            time.sleep(0.8)

        elif i ==1:
            time.sleep(2.0)
            print("Speak I am {} one more time".format(name))
            time.sleep(0.8)
        
        else:
            time.sleep(2.0)
            print("Speak I am {} one last time".format(name))
            time.sleep(0.8)
            
        stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
        
        print("recording...")
        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        waveFile = wave.open(source + '/' + str((i+1)) + '.wav', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print("Done")
        
    if not os.path.exists("./gmm_models"):
      os.mkdir("./gmm_models")
    else:
      pass
    dest =  "./gmm_models/"
    count = 1
    
    for path in os.listdir(source):
        path = os.path.join(source, path)

        features = np.array([])
        
        (sr, audio) = read(path)
        
        vector   = extract_features(audio,sr)
        
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
            
        if count == 3:    
            gmm = GMM(n_components = 16, max_iter= 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)
            
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully')
            
            features = np.asarray(())
            count = 0
        count = count + 1
        
if __name__ == '__main__':
    add_user()
