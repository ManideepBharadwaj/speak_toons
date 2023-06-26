# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:51:24 2023

@author: manideep bhardwaj
"""

import os
import openai
from ASR import asr

f = asr()

text = f.text

class chatgpt(object):
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}])
        self.gpt_response = chat_completion

if __name__ == '__main__':
    chatgpt()