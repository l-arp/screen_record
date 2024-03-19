# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:25:29 2023

@author: Örzse
"""

# %% IMPORT PACKAGES

import os

import multiprocessing
import time
import wave
from threading import Thread
from glob import glob


try:
    import pyautogui
except:
    print("\n installing pyautogui\n")
    command_install_pyautogui = "pip install PyAutoGUI"
    os.system(command_install_pyautogui)
    import pyautogui
    print("\n installed pyautogui\n")

try:
    import pyaudiowpatch as pyaudio
except:
    print("\n installing pyaudiowpatch\n")
    command_install_pyaudiowpatch = "pip install PyAudioWPatch"
    os.system(command_install_pyaudiowpatch)
    import pyaudiowpatch as pyaudio
    print("\n installed pyaudiowpatch\n")
    

try:
    from playsound import playsound
except:
    print("\n installing playsound 1.2.2\n")
    command_install_playsound = "pip install playsound==1.2.2"
    os.system(command_install_playsound)
    from playsound import playsound
    print("\n installed pyaudiowpatch\n")

try:
    from pynput.keyboard import Key, Listener
except:
    print("\n installing pynput\n")
    command_install_pynput = "pip install pynput"
    os.system(command_install_pynput)
    from pynput.keyboard import Key, Listener
    print("\n installed pynput\n")
#%% adding ffmpeg to PATH

#original_path = os.environ["PATH"]
#ffmpeg_path = os.getcwd()+"\\ffmpeg\\bin"
#os.environ["PATH"] = original_path + ";" + ffmpeg_path
    
#get_back_environment = "echo %PATH%"
#path = os.system(get_back_environment)




