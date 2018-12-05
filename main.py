from __future__ import division
import numpy as np 
import scipy.io.wavfile as wv
import matplotlib.pyplot as mp
import time
import simpleaudio as sa
import pyaudio
import tkinter as tk
from tkinter import filedialog
import filter

# f = filter.Filter() 
# 
# # a noise generation function used for testing.
# def generateRandomNoise(t):
#     t = int(t)
#     noise = np.random.normal(0,10000,(t,2))
#     return noise
# 
# # Reads the .wav file.
# audioFs, orig_audio = wv.read('serato_bigband.wav')
# #audioFs, orig_audio = 44100, generateRandomNoise(1024)
#  
# print("Working...")
# start = time.time()
# filtered = f.filter(orig_audio*1., audioFs, lowParams, midParams, highParams)
# output = np.clip(filtered, -32767, 32768)
# end = time.time() - start
# print("Done.")
# length = len(orig_audio)
# print(f"{end*audioFs:.0f} samples ({end:.3f} seconds) elapsed, processed {length:d} samples ({length/audioFs:.3f} seconds).")
#  
# # reformats the array of floating points to an array of integers.
# # plays the audio
# wave_obj = sa.WaveObject(output.astype("int16"), 2, 2, 44100)
# play_obj = wave_obj.play()
# 
# # Plots original audio and the filtered audio
# mp.figure(1)
# mp.subplot(211)
# mp.plot(orig_audio)
# mp.subplot(212)
# mp.plot(output.astype("int16"))
# mp.show()
# 
# # writes the file
# wv.write('output.wav', audioFs, output.astype("int16"))

############################### GUI CODE BELOW ##############################

types = { 'High Pass', 'Low Shelf', 'Band Pass', 'Peak', 'Notch', 'High Shelf', 'Low Pass' }

#             type            , f0  , q, gain
lowParams =  [filter.LOWSHELF , 50  , 1, 0]
midParams =  [filter.PEAK     , 500 , 1, 0]
highParams = [filter.HIGHSHELF, 5000, 1, 0]
#LOWSHELF HIGHPASS PEAK NOTCH BANDPASS LOWPASS HIGHSELF 

audioFs, orig_audio = wv.read('serato_bigband.wav')
output = orig_audio

class Band(tk.Frame):
    def __init__(self, parent, params, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.Type  = tk.StringVar(self)
        self.Freq  = tk.StringVar(self)
        self.Q     = tk.StringVar(self)
        
        self.Type.set(self.parent.master.type_to_text(params[0]))
        self.Freq.set(params[1])
        self.Q.set(params[2])
        # Band 
        self.Gain = tk.Scale(self, from_=6, to_=-30, resolution = 0.1)
        self.Gain.grid(row = 0, column = 2, rowspan = 3)
        self.Gain.set(params[3])
        tk.Label(self, text="Type: ",font = "Arial 12").grid(row = 0, column = 0, sticky='w')
        self.TypeMenu = tk.OptionMenu(self, self.Type, *types)
        self.TypeMenu.grid(row = 0, column = 1, sticky='ew')
        tk.Label(self, text="Freq: ",font = "Arial 12").grid(row = 1, column = 0, sticky='w')
        self.FreqBox = tk.Entry(self, textvariable = self.Freq)
        self.FreqBox.grid(row = 1, column = 1)
        tk.Label(self, text="Q: ",font = "Arial 12").grid(row = 2, column = 0, sticky='w')
        self.QBox = tk.Entry(self, textvariable = self.Q)
        self.QBox.grid(row = 2, column = 1)
        # lowQ = tk.Scale (b1Grid, from_=0.1, to_=4, orient='horizontal', resolution = 0.1)
        # lowQ.grid(row = 2, column =1)
        
class ButtonGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.applyButton = tk.Button(self, text="Apply", command=parent.apply)
        self.applyButton.grid(row = 0, column = 0, sticky='ew')
        
        self.resetButton = tk.Button(self, text="Reset", command=parent.reset_params)
        self.resetButton.grid(row = 0, column = 1, sticky='ew')
        
        self.playButton = tk.Button(self, text="Play", command=parent.play)
        self.playButton.grid(row = 1, column = 0, sticky='ew')
        
        self.stopButton = tk.Button(self, text="Stop", command=parent.stop)
        self.stopButton.grid(row = 1, column = 1, sticky='ew')
        
        self.saveButton = tk.Button(self, text="Save", command=parent.save)
        self.saveButton.grid(row = 2, column = 0, sticky='ew')
        
        self.loadButton = tk.Button(self, text="Load", command=parent.load)
        self.loadButton.grid(row = 2, column = 1, sticky='ew')
        
class MainApplication(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.filepath = 'serato_bigband.wav'
        self.parent = parent
        self.config(bg="light blue")
        tk.Label(self, text="Parametric EQ", font = "Arial 20 bold", bg="light blue").grid(row = 0, column = 1, ipady = 5)
        
       
        b1window = tk.PanedWindow(self, orient ='vertical')
        b1window.grid(row = 1, column = 0, padx = 5, pady = 5)
        b1Label = tk.Label(b1window, text="Band 1", font = "Arial 16 bold italic")
        self.b1 = Band(b1window, lowParams)
        b1window.add(b1Label)
        b1window.add(self.b1)
        
        b2window = tk.PanedWindow(self, orient ='vertical')
        b2window.grid(row = 1, column = 1, padx = 5, pady = 5)
        b2Label = tk.Label(b2window, text="Band 2", font = "Arial 16 bold italic")
        self.b2 = Band(b2window, midParams)
        b2window.add(b2Label)
        b2window.add(self.b2)
        
        b3window = tk.PanedWindow(self, orient ='vertical')
        b3window.grid(row = 1, column = 2, padx = 5, pady = 5)
        b3Label = tk.Label(b3window, text="Band 3", font = "Arial 16 bold italic")
        self.b3 = Band(b3window, highParams)
        b3window.add(b3Label)
        b3window.add(self.b3)
        
        buttons = ButtonGrid(self)
        buttons.grid(row = 1, column = 3, padx = 10, pady = 10)      
        
    def update_params(self):
        global lowParams, midParams, highParams
        lowParams = [self.text_to_type(self.b1.Type.get()), int(self.b1.Freq.get()), float(self.b1.Q.get()), self.b1.Gain.get()];
        midParams = [self.text_to_type(self.b2.Type.get()), int(self.b2.Freq.get()), float(self.b2.Q.get()), self.b2.Gain.get()];
        highParams = [self.text_to_type(self.b3.Type.get()), int(self.b3.Freq.get()), float(self.b3.Q.get()), self.b3.Gain.get()];
        
        return
    
    def apply(self):
        global orig_audio, audioFs, output, lowParams, midParams, highParams
        self.update_params()
        
        f = filter.Filter() 
        print("Working...")
        start = time.time()
        filtered = f.filter(orig_audio*1., audioFs, lowParams, midParams, highParams)
        output = np.clip(filtered, -32767, 32768)
        end = time.time() - start
        print("Done.")
        length = len(orig_audio)
        print(f"{end*audioFs:.0f} samples ({end:.3f} seconds) elapsed, processed {length:d} samples ({length/audioFs:.3f} seconds).")

        return
    def play(self):
        global output
        self.wave_obj = sa.WaveObject(output.astype("int16"), 2, 2, 44100)
        self.play_obj = self.wave_obj.play()
        return
    def stop(self):
        try:
            if self.play_obj.is_playing():
                self.play_obj.stop()
        finally:
            return
    def save(self):
        global audioFs, output
        filepath = self.filepath[0:self.filepath.rfind('/')+1]
        print(filepath)
        wv.write(filepath+'output.wav', audioFs, output.astype("int16"))
        return
    def load(self):
        self.filepath = filedialog.askopenfilename(initialdir= "/", title = "Select .wav file", filetypes = ((".WAV files","*.wav"),("all files","*.*")))
        global audioFs, orig_audio, output
        audioFs, orig_audio = wv.read(self.filepath)
        output = orig_audio
        return
    def reset_params(self):
        self.b1.Gain.set(0)
        self.b2.Gain.set(0)
        self.b3.Gain.set(0)
        self.b1.Freq.set(50)
        self.b2.Freq.set(500)
        self.b3.Freq.set(5000)
        self.b1.Q.set(1)
        self.b2.Q.set(1)
        self.b3.Q.set(1)
        self.b1.Type.set("Low Shelf")
        self.b2.Type.set("Peak")
        self.b3.Type.set("High Shelf")
        
        self.update_params()
        
        global output
        output = orig_audio
        return
    def text_to_type(self, arg): 
        switcher = { 
            "High Shelf":filter.HIGHSHELF,
            "Low Shelf":filter.LOWSHELF,
            "Peak":filter.PEAK,
            "Notch":filter.NOTCH,
            "Low Pass":filter.LOWPASS,
            "High Pass":filter.HIGHPASS,
            "Band Pass":filter.BANDPASS,
        } 
        return switcher.get(arg, filter.LOWSHELF) 
    
    def type_to_text(self, arg): 
        switcher = { 
            filter.HIGHSHELF:"High Shelf",
            filter.LOWSHELF:"Low Shelf",
            filter.PEAK:"Peak",
            filter.NOTCH:"Notch",
            filter.LOWPASS:"Low Pass",
            filter.HIGHPASS:"High Pass",
            filter.BANDPASS:"Band Pass",
        } 
        return switcher.get(arg, "Low Shelf") 
    
        #highparams = [self.text_to_type(highTyp), int(highFreq.get()), int(highQ.get()), self.highGain.get()]
# infinite loop () a must for self)
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.resizable(width=False, height=False)
    root.title("Parametric EQ")
    root.mainloop()



