# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 12:17:14 2023

@author: manideep bhardwaj
"""

import pyttsx3

from chatgpt import chatgpt

f = chatgpt()

class text_to_speech():
    def __init__(self):
        text = f.gpt_response
        engine = pyttsx3.init()
        engine.save_to_file(text, 'speech.wav')
        engine.runAndWait()

if __name__ == '__main__':
    text_to_speech()