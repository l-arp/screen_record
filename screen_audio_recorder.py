# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 22:31:00 2023

@author: larpi
"""

# %% IMPORTS
from tkinter import Tk, Frame, Entry, Label, Button
import os
import time
import subprocess
from playsound import playsound
from threading import Thread
import pyaudiowpatch as pyaudio
import wave
import pywintypes
import win32api
import win32con
from pynput.keyboard import Key, Listener


#%% KEYBOARD DETECTION FUNCTION
def on_release(key):
#    print('{0} release'.format(
#        key))
    if key ==Key.alt_gr:
            # Stop listener
        return False
# %% SCREEN CAPTURE
def video_capture(duration,FPS,ffmeg_exe_loc, start_time,show_mouse):
    # sleep time for synchronous start (with audio record)
    while (time.time_ns()-start_time<5*10**9):
        time.sleep(10**-9)
        
#     for debugging
#    start_time = start_time/10**9
        
    # log video record start
    log = open("log.txt","a")
    log.write("\n\nvideo record started:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
    log.close()
    
    curr_dir = os.getcwd()
    # ffmpeg script for screen recording (udemy)
    # subprocess.run/subprocess.Popen does not launch cmd window
    # "FFMPEG - The Complete Complete Guide" by Syed Andaleeb Roomy
#    subprocess.run(["{}".format(ffmeg_exe_loc), "-y", "-rtbufsize", "100M", "-f", "gdigrab", "-t", "{}".format(duration), "-framerate", "{}".format(FPS), "-probesize", "10M", "-draw_mouse", "1", "-i", "desktop", "-c:v", "libx264", "-r", "{}".format(FPS), "-preset", "ultrafast", "-tune", "zerolatency", "-crf", "25", "-pix_fmt", "yuv420p", "c:\\python\\video.mp4"])
    output_name = curr_dir + "\\video.mp4"
    p = subprocess.Popen(["{}".format(ffmeg_exe_loc), "-y", "-rtbufsize", "100M", "-f", "gdigrab", "-t", "{}".format(duration), "-framerate", "{}".format(FPS), "-probesize", "10M", "-draw_mouse", "{}".format(show_mouse), "-i", "desktop", "-c:v", "libx264", "-r", "{}".format(FPS), "-preset", "ultrafast", "-tune", "zerolatency", "-crf", "25", "-pix_fmt", "yuv420p", "{}".format(output_name)],
                            shell=True,
                            stderr=subprocess.STDOUT,
                            stdin=subprocess.PIPE)
    p.stdin.close()
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
    
    
    
    

    # log video record start
    log = open("log.txt","a")
    log.write("\n\nvideo record finished:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
    log.close()
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
    # log video record start
    log = open("log.txt","a")
    log.write("\n\naudio record started:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
    log.close()
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
        
    # log video record start
    log = open("log.txt","a")
    log.write("\n\naudio record finished:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
    log.close()

#%% VOICE FUNCTIONS
def countdown(start_time):
    while True:
        if time.time_ns()>start_time+10**9:
            playsound('countdown_4_sec.wav')
            return
def end_voice():
    playsound("recording_finished.wav")

def merging(video_input, audio_input, merged_output, ffmpeg_exe_loc):
    # log after recording
    log = open("log.txt","a")
    log.write("\nrecording finished:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
    log.close()
    # put current time to output file name
    merged_output = merged_output.split(".")
    # in year month day hour minute second format
    merged_output = merged_output[0]+"_"+time.strftime("%Y_%m_%d_%H_%M_%S")+"."+merged_output[1]
    # ffmpeg command for merging audio and screen record
    # note: this pops up cmd window
    
    curr_dir = os.getcwd()
    subprocess.Popen(["{}".format(ffmpeg_exe_loc), "-y", "-i", "{}".format(video_input), "-i", "{}".format(audio_input), "-c:v", "copy","-c:a", "aac", "{}".format(merged_output)],cwd=curr_dir,shell=True) 
    
    # log after audio-video merging
    log = open("log.txt","a")
    log.write("\nmerging finished:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
    log.close()    
        

# %% TKINTER FUNCTIONS

# frame change 
def raise_frame(frame):
    frame.tkraise()

def start_record():
    global entry
    try:
        # kill tkinter window       
        root.destroy()
        
        # log at before recording + overwrite previous log
        log = open("log.txt","w")
        log.write("\n\nRecording process started:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
        log.close()
        
        # recording params
        ffmeg_exe_loc = os.getcwd()+"\\ffmpeg\\bin\\ffmpeg.exe"
        output_format = ".mp4"
        file = open("params.txt", "r")
        params = file.read()
        
        duration = params.split("duration=")[1].split(" ")[0]
        duration = float(duration)
        FPS = params.split("framerate=")[1].split(" ")[0]
        FPS = float(FPS)
        file.close()
        
        show_mouse = 0 # 0: do not show 1: show        
        
        start_time = time.time_ns()
        
        # call recording functions
        countdown_at_start = Thread(target=countdown,args=(start_time,))
        countdown_at_start.start()        
        audio = Thread(target=audio_record, args=(duration,start_time))
        audio.start()
        video_capture(duration,FPS,ffmeg_exe_loc,start_time,show_mouse)
        audio.join() 

        # video-audio merging params
        curr_dir = os.getcwd()
        output_format = ".mp4"
        video_input = "\\video.mp4"
        audio_input = "\\audio.wav"
        merged_output = "\\video_record" + output_format
        ffmpeg_exe_loc = "\\ffmpeg\\bin\\ffmpeg.exe"
        
        video_input = curr_dir + video_input
        audio_input =  curr_dir + audio_input
        merged_output =  curr_dir + merged_output
        ffmpeg_exe_loc = curr_dir + ffmpeg_exe_loc
        # call merging function
        merging(video_input, audio_input, merged_output, ffmpeg_exe_loc)
#        curr_dir = os.getcwd()
#        process = subprocess.Popen("python ffmpeg_record_with_txt.py", cwd=curr_dir)
#        process.wait()
        
#        # log after recording
#        log = open("log.txt","a")
#        log.write("\nrecording finished:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
#        log.close()
#        
#        output_format = ".mp4"
#        video_input = "\\video.mp4"
#        audio_input = "\\audio.wav"
#        merged_output = "\\video_record" + output_format
#        ffmpeg_exe_loc = "\\ffmpeg\\bin\\ffmpeg.exe"
#        curr_dir = os.getcwd()
#        os.chdir(curr_dir)
##        command = "python ffmpeg_merging.py "+"'"+video_input+"' '"+audio_input+"' '"+merged_output+"' '"+ffmpeg_exe_loc+"'"
##        os.system(command)
#        video_input = curr_dir + video_input
#        audio_input =  curr_dir + audio_input
#        merged_output =  curr_dir + merged_output
#        merged_output = merged_output.split(".")
#         in year month day hour minute second format
#        merged_output = merged_output[0]+"_"+time.strftime("%Y_%m_%d_%H_%M_%S")+"."+merged_output[1]
#        ffmpeg_exe_loc = curr_dir + ffmpeg_exe_loc
#        subprocess.Popen(["{}".format(ffmpeg_exe_loc), "-y", "-i", "{}".format(video_input), "-i", "{}".format(audio_input), "-c:v", "copy","-c:a", "aac", "{}".format(merged_output)],cwd=curr_dir)         
#        # log after audio-video merging
#        log = open("log.txt","a")
#        log.write("\nmerging finished:\n\t {} local time\n\t {} [ns] (since epoch)".format(time.ctime(),time.time_ns()))
#        log.close()            
    # check input params
    except Exception as e:
       print("\nError: {}\n".format(e))
        
def raise_start_frame(frame):
   global entry
   try:
       hour = int(entry_i_h.get())
       minute = int(entry_i_m.get())
       second = int(entry_i_s.get())
       fps = float(entry_i_fps.get())
       if (minute>59 or second>59 or hour<0 or minute<0 or second<0):
           print("\nERROR: minutes and seconds must be between 0 and 59!!\n")
       elif(fps<1 or fps>240):
           print("\nERROR: FPS must be between 1 and 240!!\n")
       else:
           print("hours: {}\nminutes: {}\nsecond:{}".format(hour,minute,second))
           print("seconds: {}".format(hour*3600+minute*60+second))
           frame.tkraise()
           label_s=Label(start, text="Hours: {} \nMinutes: {} \nSeconds: {}\nFPS: {}\n".format(hour,minute,second,fps), font=('Arial', 16))
           label_s.place(x=200,y=65)
           
       file = open("params.txt","w")
       file.write("duration={} [s],framerate={} [FPS]".format(hour*3600+minute*60+second, fps))
       file.close()
        
       # raise_frame2()
   except Exception as e:
       print("\nError: {}\n".format(e))
   
#%% FRAMES
root = Tk()

root.geometry("500x500")

#  4 frames:
#  INIT: initialize record parameters:
    # video length in hour/min/sec
    # FPS
    # screen size
    
init = Frame(root,width=600, height=600)
init.pack_propagate(0)
init.pack(fill=None, expand=False)

# START:
    # give feedback about parameters given in INIT
    # start record at button pressing
    # switch to PROGRESS if everything is OK
    # NOK -> INIT
start = Frame(root,width=600, height=600)

# PROGRESS:
    # TODO!
    # disappear (for duration???)
progress = Frame(root,width=600, height=600)

# DONE:
    # feedback about result (file size)
    # option to record again
done = Frame(root,width=600, height=600)

for frame in (init, start, progress, done):
    frame.grid(row=0, column=0, sticky='news')

# -----------------------------------------------------------------------
      
# INIT entrys:
    # hour entry
entry_i_h = Entry(init,width=3, font=('Arial 16'))
entry_i_h.focus_set()
# entry_h.pack()
entry_i_h.place(x=180,y=50)
    # minute entry
entry_i_m = Entry(init,width=3, font=('Arial 16'))
entry_i_m.focus_set()
entry_i_m.pack()
entry_i_m.place(x=10,y=50)
entry_i_m.place(x=180,y=100)
    # second entry
entry_i_s= Entry(init,width=3, font=('Arial 16'))
entry_i_s.focus_set()
entry_i_s.pack()
entry_i_s.place(x=180,y=150)
    # fps entry
entry_i_fps= Entry(init,width=5, font=('Arial 16'))
entry_i_fps.focus_set()
entry_i_fps.pack()
entry_i_fps.place(x=330,y=150)

# INIT LABELS
    # main label
l_i_1 = Label(init, text='Initialize recording parameters')
l_i_1.config(font =("Arial", 16))
l_i_1.place(x=20, y=10)
    # hour label
l_i_h = Label(init, text='Hours:')
l_i_h.config(font =("Arial", 16))
l_i_h.place(x=80, y=47)
    # minute label
l_i_m = Label(init, text='Minutes:')
l_i_m.config(font =("Arial", 16))
l_i_m.place(x=60, y=97)
    # second label
l_i_s = Label(init, text='Seconds:')
l_i_s.config(font =("Arial", 16))
l_i_s.place(x=55, y=147)
    # FPS label
l_i_fps = Label(init, text='FPS:')
l_i_fps.config(font =("Arial", 16))
l_i_fps.place(x=255, y=147)

# INIT BUTTONS
button_i_next = Button(init, text='Next', padx=35, pady=35, command=lambda:raise_start_frame(start))
button_i_next.place(x=250, y=250)

# -----------------------------------------------------------------------

# START LABELS
    # main label
l_s_1 = Label(start, text='Your parameters:')
l_s_1.config(font =("Arial", 16))
l_s_1.place(x=20, y=10)

# START BUTTONS

button_s_go = Button(start, text='Start record',padx=35, pady=35, command=lambda:start_record())
button_s_go.place(x=300, y=250)
button_s_back = Button(start, text='Back',padx=35, pady=35, command=lambda:raise_frame(init))
button_s_back.place(x=50, y=250)

# debug
# # Progress frame
# Label(progress, text='Progress').pack(side='left')
# Button(progress, text='Next', command=lambda:raise_frame(done)).pack(side='left')


# # End frame
# Label(done, text='Done').pack()
# Button(done, text='End', command=lambda:raise_frame(init)).pack()
# debug end

raise_frame(init)

root.mainloop()