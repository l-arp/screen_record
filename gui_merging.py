# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 22:31:00 2023

@author: larpi
"""

# %% IMPORTS
from tkinter import Tk, Frame, Entry, Label, Button
import os
import subprocess as sp
import time
import ffmpeg_record_with_txt
import subprocess


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
    
# %% FUNCTIONS

# frame change 
def raise_frame(frame):
    frame.tkraise()

def start_record():
    global entry
    try:
#        almost good but window must be hidden
        root.destroy()
#        curr_dir = os.getcwd()
#        os.chdir(curr_dir)
#        command = "python ffmpeg_record_with_txt.py"
#        os.system(command)
        

        
#        # kill all windows
#        root.destroy()
#        #get current directory
        curr_dir = os.getcwd()
#        # and run recording script while being in this folder
#        # -> ffmpeg and other files are found (start countdown, ending voice, ...)
        process = subprocess.Popen("python ffmpeg_record_with_txt.py", cwd=curr_dir)
        process.wait()
#        with open("ffmpeg_record_with_txt.py") as f:
#            exec(f.read())
        
        # ITT VÁRAKOZÁS ADDIG AMÍG NINCS VÉGE SUBPROCESSNEK
        
        output_format = ".mp4"
        video_input = "\\video.mp4"
        audio_input = "\\audio.wav"
        merged_output = "\\video_record" + output_format
        ffmeg_exe_loc = "\\ffmpeg\\bin\\ffmpeg.exe"
        curr_dir = os.getcwd()
        os.chdir(curr_dir)
        command = "python ffmpeg_merging.py "+"'"+video_input+"' '"+audio_input+"' '"+merged_output+"' '"+ffmeg_exe_loc+"'"
        os.system(command)            
            
            
            
#        frame.tkraise()
#        import time
#        import ffmpeg_record
#        import multiprocessing
#        
#        if __name__ == '__main__':
#            with multiprocessing.Manager() as manager:
#                print("loop started\n")
#                duration = 10
#                FPS = 30
#                show_cursor = 0
#                start_time = time.time_ns()
#                video = multiprocessing.Process(target=ffmpeg_record.video_capture, args=(duration,FPS,start_time, show_cursor))
#                audio = multiprocessing.Process(target=ffmpeg_record.audio_record, args=(duration,start_time))
#                print("record started\n")
#                video.start()
#                audio.start()
#                print("start OK\n")
#                video.join()
#                audio.join()
#            print("record ended\n")
#        ffmpeg_record.merging("video.mp4","audio.wav","Arpi_teszt.mp4")
            # with multiprocessing.Manager() as manager:
            #     duration = 10
            #     FPS = 30
            #     show_cursor = 0
            #     start_time = time.time_ns()
            #     video = multiprocessing.Process(target=ffmpeg_record.video_capture(duration,FPS,start_time, show_cursor), args=(duration,FPS,start_time, show_cursor))
            #     audio = multiprocessing.Process(target=ffmpeg_record.audio_record(duration,start_time), args=(duration,start_time))
                
            #     video.start()
            #     audio.start()
                
                # video.join()
                # audio.join()
        # os.system('python dxcam_test.py')
    #     p = sp.Popen(
    #     ["python", "fmmpeg_record.py"], 
    #     stdout=sp.PIPE, stderr=sp.PIPE, text=True
    # )
    #     while True:
    #         print(p)
    #         time.sleep(1)
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