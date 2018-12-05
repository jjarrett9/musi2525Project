from __future__ import division
import numpy as np 
import scipy.io.wavfile as wv
import matplotlib.pyplot as mp
import time
import simpleaudio as sa
import pyaudio
import tkinter as tk
import filter
types = { 'High Pass', 'Low Shelf', 'Band Pass', 'Peak', 'Notch', 'High Shelf', 'Low Pass' }

#             type            , f0  , q, gain
lowParams =  [filter.LOWSHELF , 50  , 1, 0]
midParams =  [filter.PEAK     , 500 , 1, 0]
highParams = [filter.HIGHSHELF, 5000, 1, 0]
# 
# f = filter.Filter()
# 
# def generateRandomNoise(t):
#     t = int(t)
#     noise = np.random.normal(0,10000,(t,2))
#     return noise

# #Replace this with file read button
# #audioFs, orig_audio = wv.read('serato_bigband.wav')
# #audioFs, orig_audio = 44100, generateRandomNoise(1024)
# #Replace this with self and such

# print("Working...")
# start = time.time()
# #Replace this with self and such
# filtered = f.filter(orig_audio*1., audioFs, lowParams, midParams, highParams)
# 
# output = np.clip(filtered, -32767, 32768)
# end = time.time() - start
# print("Done.")
# 
# length = len(orig_audio)
# print(f"{end*audioFs:.0f} samples ({end:.3f} seconds) elapsed, processed {length:d} samples ({length/audioFs:.3f} seconds).")
# 
# wave_obj = sa.WaveObject(output.astype("int16"), 2, 2, 44100)
# play_obj = wave_obj.play()

# # Remove this later
# mp.figure(1)
# mp.subplot(211)
# mp.plot(orig_audio)
# mp.subplot(212)
# mp.plot(output.astype("int16"))
# mp.show()

# wv.write('lp_serato2.wav', audioFs, output.astype("int16"))

class Band(tk.Frame):
    def __init__(self, parent, type, freq, q, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.Type  = tk.StringVar(self)
        self.Freq  = tk.StringVar(self)
        self.Q     = tk.StringVar(self)
        
        self.Type.set(type)
        self.Freq.set(freq)
        self.Q.set(q)
        # Band 
        self.Gain = tk.Scale(self, from_=6, to_=-30, resolution = 0.1)
        self.Gain.grid(row = 0, column = 2, rowspan = 3)
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
        
class MainApplication(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.parent = parent
        
        tk.Label(self, text="Parametric EQ", font = "Arial 20 bold").grid(row = 0, column = 1, ipady = 5)
        
       
        b1window = tk.PanedWindow(self, orient ='vertical')
        b1window.grid(row = 1, column = 0, padx = 5, pady = 5)
        b1Label = tk.Label(b1window, text="Band 1", font = "Arial 16 bold")
        self.b1 = Band(b1window, filter.LOWSHELF, 50, 1)
        b1window.add(b1Label)
        b1window.add(self.b1)
        
        b2window = tk.PanedWindow(self, orient ='vertical')
        b2window.grid(row = 1, column = 1, padx = 5, pady = 5)
        b2Label = tk.Label(b2window, text="Band 2", font = "Arial 16 bold")
        self.b2 = Band(b2window, filter.PEAK, 500, 1)
        b2window.add(b2Label)
        b2window.add(self.b2)
        
        b3window = tk.PanedWindow(self, orient ='vertical')
        b3window.grid(row = 1, column = 2, padx = 5, pady = 5)
        b3Label = tk.Label(b3window, text="Band 3", font = "Arial 16 bold")
        self.b3 = Band(b3window, filter.PEAK, 500, 1)
        b3window.add(b3Label)
        b3window.add(self.b3)
    
    def text_to_type(argument): 
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
    
    def type_to_text(argument): 
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
    
    def update_high_params(self, event=0):
        global highParams
        print(self.highGain.get())
        #highparams = [self.text_to_type(highTyp), int(highFreq.get()), int(highQ.get()), self.highGain.get()]
# infinite loop () a must for self)
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.resizable(width=False, height=False)
    root.title("Parametric EQ")
    root.mainloop()



