# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 19:16:09 2023

@author: larpi
"""

# %%

import multiprocessing
import pyautogui
import time
import os
import pyaudiowpatch as pyaudio
import time
import wave
from threading import Thread
from playsound import playsound
import subprocess

import pywintypes
import win32api
import win32con

import sys
from pynput.keyboard import Key, Listener

import signal

# DETECT KEYS

#def on_press(key):
#    print('{0} pressed'.format(
#        key))

# ONLY DETECT RELEASE
def on_release(key):
#    print('{0} release'.format(
#        key))
    if key ==Key.alt_gr:
            # Stop listener
        return False
  
# %% AUDIO + VIDEO MERGING
#        IN SEPERATE MODULE
#def merging(video_input, audio_input, merged_output, ffmeg_exe_loc):
#    print("\nMerge started {}\n".format(time.ctime()))
#    # put current time to output file name
#    merged_output = merged_output.split(".")
#    # in year month day hour minute second format
#    merged_output = merged_output[0]+"_"+time.strftime("%Y_%m_%d_%H_%M_%S")+"."+merged_output[1]
#    # ffmpeg command for merging audio and screen record
#    # note: this pops up cmd window
#    
#    curr_dir = os.getcwd()
#    subprocess.Popen(["{}".format(ffmeg_exe_loc), "-y", "-i", "{}".format(video_input), "-i", "{}".format(audio_input), "-c:v", "copy","-c:a", "aac", "{}".format(merged_output)],cwd=curr_dir) 
#    print("\nMerge finished {}\n".format(time.ctime()))
##    command_merge = '{0} -y -i {1} -i {2} -c:v copy -c:a aac {3}'.format(ffmeg_exe_loc, video_input,audio_input,merged_output)
##    os.system(command_merge)
    
# %% SCREEN CAPTURE
def video_capture(duration,FPS,ffmeg_exe_loc, start_time,show_mouse):
    # sleep time for synchronous start (with audio record)
    while (time.time_ns()-start_time<5*10**9):
        time.sleep(10**-9)
        
#     for debugging
#    start_time = start_time/10**9
    print('Video capture: Started {}'.format(time.ctime()))
    
    curr_dir = os.getcwd()
    # ffmpeg script for screen recording (udemy)
    # subprocess.run/subprocess.Popen does not launch cmd window
    # "FFMPEG - The Complete Complete Guide" by Syed Andaleeb Roomy
#    subprocess.run(["{}".format(ffmeg_exe_loc), "-y", "-rtbufsize", "100M", "-f", "gdigrab", "-t", "{}".format(duration), "-framerate", "{}".format(FPS), "-probesize", "10M", "-draw_mouse", "1", "-i", "desktop", "-c:v", "libx264", "-r", "{}".format(FPS), "-preset", "ultrafast", "-tune", "zerolatency", "-crf", "25", "-pix_fmt", "yuv420p", "c:\\python\\video.mp4"])
    output_name = curr_dir + "\\video.mp4"
    p = subprocess.Popen(["{}".format(ffmeg_exe_loc), "-y", "-rtbufsize", "100M", "-f", "gdigrab", "-t", "{}".format(duration), "-framerate", "{}".format(FPS), "-probesize", "10M", "-draw_mouse", "{}".format(show_mouse), "-i", "desktop", "-c:v", "libx264", "-r", "{}".format(FPS), "-preset", "ultrafast", "-tune", "zerolatency", "-crf", "25", "-pix_fmt", "yuv420p", "{}".format(output_name)])
    
    # start keyboard listening
    listener_video = Listener(on_release=on_release)
    listener_video.start()
    start_time = time.time()
    # if alt_gr is pressed or recording time is up
    while time.time()-start_time < duration+5 and listener_video.isAlive():
        time.sleep(0.1)
    # break keyboard listening
    listener_video.stop()
    # THIS IS OK but python script should not be included
#    subprocess.check_call([sys.executable, 'ctrl_c.py', str(p.pid)])

    if time.time()-start_time < duration+5:
        import ctypes
        
        kernel = ctypes.windll.kernel32
        
        pid = p.pid
        print(f"Send Ctrl+C to pid: {pid}")
        kernel.FreeConsole()
        kernel.AttachConsole(pid)
        kernel.SetConsoleCtrlHandler(None, 1)
        kernel.GenerateConsoleCtrlEvent(0, 0)
#        sys.exit()
        quit()
    
    
    
    

    print('Video capture: finished {}'.format(time.ctime()))
# %% AUDIO RECORD FUNCTION
def sound(duration):
    # background sound (low volume, not noticable)
    # sound record does not start if there is no system sound
    start_time = time.time()
    while time.time()-start_time<duration:
        playsound('intro.wav')
        
def audio_record(duration,start_time):
    sound_for_start = Thread(target=sound,args=(duration,))
    sound_for_start.start()
    while (time.time_ns()-start_time<5*10**9):
        time.sleep(10**-9)
    filename = "audio.wav"
    DURATION = duration
    CHUNK_SIZE = 512
#     for debugging
    print('Audio record: Started {}'.format(time.time_ns()))
    # from stackoverflow
    with pyaudio.PyAudio() as p:
        """
        Create PyAudio instance via context manager.
        Spinner is a helper class, for `pretty` output
        """
        try:
            # Get default WASAPI info
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            # spinner.print("Looks like WASAPI is not available on the system. Exiting...")
            # spinner.stop()
            exit()
        
        # Get default WASAPI speakers
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                """
                Try to find loopback device with same name(and [Loopback suffix]).
                Unfortunately, this is the most adequate way at the moment.
                """
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
            else:
                # spinner.print("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")
                # spinner.stop()
                exit()
                
        # spinner.print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")
        
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(default_speakers["maxInputChannels"])
        wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(int(default_speakers["defaultSampleRate"]))
        
        def callback(in_data, frame_count, time_info, status):
            """Write frames and return PA flag"""
            wave_file.writeframes(in_data)
            return (in_data, pyaudio.paContinue)
        
        with p.open(format=pyaudio.paInt16,
                channels=default_speakers["maxInputChannels"],
                rate=int(default_speakers["defaultSampleRate"]),
                frames_per_buffer=CHUNK_SIZE,
                input=True,
                input_device_index=default_speakers["index"],
                stream_callback=callback
        ) as stream:
            """
            Opena PA stream via context manager.
            After leaving the context, everything will
            be correctly closed(Stream, PyAudio manager)            
            """
            # spinner.print(f"The next {DURATION} seconds will be written to {filename}")
            
            
            # időközönként chekkolni hogy érkezett-e exit
            
#            time.sleep(DURATION) # Blocking execution while playing
            start_time = time.time()
            # start keyboard listening
            listener_audio = Listener(on_release=on_release)
            listener_audio.start()
            # if alt_gr is pressed or recording time is up
            while time.time()-start_time < DURATION and listener_audio.isAlive():
                time.sleep(0.1)
            # break keyboard listening
            listener_audio.stop()
        recording_end_voice = Thread(target=end_voice,args=())
        recording_end_voice.start()
        wave_file.close()  
#     for debuging
    print('Audio record: finished {}'.format(time.ctime()))

#%% COUNTDOWN AT START
def countdown(start_time):
    while True:
        if time.time_ns()>start_time+10**9:
            playsound('countdown_4_sec.wav')
            return
def end_voice():
    playsound("recording_finished.wav")
# %% MAIN FUNCTION
if __name__ == '__main__':
    print("\n\n")
    print(os.getcwd())
    print(os.path.abspath('params.txt'))
    print("\n\n")
    # TODO:
    # - press to end recording (DONE)
    # - merge function with Popen (DONE)
    # - change screen size (DONE)
    # - change format (DONE)
    # - cutting
    # - start & end voice (DONE) end voice can be timed better
    

    
#     for debugging
    print('Process started: {}'.format(time.ctime())) 
    
    # input parameters
    ffmeg_exe_loc = os.getcwd()+"\\ffmpeg\\bin\\ffmpeg.exe"
    output_format = ".mp4"
#    FPS = 60
#    duration = 20
    file = open("params.txt", "r")
    params = file.read()
    
    duration = params.split("duration=")[1].split(" ")[0]
    duration = float(duration)
    FPS = params.split("framerate=")[1].split(" ")[0]
    FPS = float(FPS)
    file.close()
    
    show_mouse = 0 # 0: do not show 1: show
#    screen_width = 800
#    screen_height = 600
    screen_width = 1366
    screen_height = 768
    
    
    # debug start
#    video_input = "C:\\python\\video.mp4"
#    audio_input = "C:\\python\\audio.wav"
#    merged_output = "C:\\python\\video_record" + output_format
#    merging(video_input, audio_input, merged_output, ffmeg_exe_loc)
#    
#    time.sleep(60)
    # debug end
    # screen size can be used in the future to change resolution -> smaller file size
    SCREEN_SIZE = tuple(pyautogui.size())
    # if new screen resolution is different than current one change it
    if screen_width!=SCREEN_SIZE[0] or screen_height!=SCREEN_SIZE[1]:
        devmode = pywintypes.DEVMODEType()
        devmode.PelsWidth = screen_width
        devmode.PelsHeight = screen_height

        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
        
        win32api.ChangeDisplaySettings(devmode, 0)
        # extra sleep time before starting
        time.sleep(2)
        
        
        
    with multiprocessing.Manager() as manager:
        start_time = time.time_ns()
        countdown_at_start = Thread(target=countdown,args=(start_time,))
        countdown_at_start.start()        
        audio = multiprocessing.Process(target=audio_record, args=(duration,start_time))
        audio.start()
        video_capture(duration,FPS,ffmeg_exe_loc,start_time,show_mouse)
        audio.join()
#     for debugging
    print('Process finished: {}'.format(time.ctime()))
#    end_voice()
#    recording_end_voice = Thread(target=end_voice,args=())
#    recording_end_voice.start()
#    video_input = os.getcwd() + "\\video.mp4"
#    audio_input = os.getcwd() + "\\audio.wav"
#    merged_output = os.getcwd() + "\\video_record" + output_format
##    video_input = "C:\\python\\video.mp4"
##    audio_input = "C:\\python\\audio.wav"
##    merged_output = "C:\\python\\video_record" + output_format
#    merging(video_input, audio_input, merged_output, ffmeg_exe_loc)
#    
##     for debugging
#    print('Video merging finished: {}'.format(time.ctime()))
#    
    # change back screen resolution if it was changed
    if screen_width!=SCREEN_SIZE[0] or screen_height!=SCREEN_SIZE[1]:    
        win32api.ChangeDisplaySettings(None, 0)
    
    # így se jó, nics hibaüzenet
#    curr_dir = os.getcwd() 
#    subprocess.Popen(["{}".format(ffmeg_exe_loc), "-y", "-i", "{}".format(video_input), "-i", "{}".format(audio_input), "-c:v", "copy","-c:a", "aac", "{}".format(merged_output)],cwd=curr_dir)
#    time.sleep(60)
    # így se jó, nics hibaüzenet
    