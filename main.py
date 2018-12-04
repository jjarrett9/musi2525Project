from __future__ import division
import numpy as np 
import scipy.io.wavfile as wv
import matplotlib.pyplot as mp
import time
import simpleaudio as sa
import pyaudio
from tkinter import *

import filter

#             type            , f0  , q, gain
lowParams =  [filter.LOWSHELF , 50  , 1, 0]
midParams =  [filter.PEAK     , 500 , 1, 0]
highParams = [filter.HIGHSHELF, 5000, 1, 0]


f = filter.Filter()

def generateRandomNoise(t):
    t = int(t)
    noise = np.random.normal(0,10000,(t,2))
    return noise

#Replace this with file read button
#audioFs, orig_audio = wv.read('serato_bigband.wav')
audioFs, orig_audio = 44100, generateRandomNoise(1024)


#Replace this with GUI and such
f0 = eval(input("Enter center frequency: "))
q = eval(input("Enter filter Q: "))
g = eval(input("Enter gain: "))

print("Working...")
start = time.time()
#Replace this with GUI and such
filtered = f.filter(orig_audio*1., audioFs, lowParams, midParams, highParams)

output = np.clip(filtered, -32767, 32768)
end = time.time() - start
print("Done.")

length = len(orig_audio)
print(f"{end*audioFs:.0f} samples ({end:.3f} seconds) elapsed, processed {length:d} samples ({length/audioFs:.3f} seconds).")

wave_obj = sa.WaveObject(output.astype("int16"), 2, 2, 44100)
play_obj = wave_obj.play()


GUI = Tk()
GUI.geometry("600x400+300+300")
GUI.configure(background='gray')
GUI.title("Parametric EQ")
Label(GUI, 
         text="Parametric EQ",
         fg = "white",
         bg = "gray",
         font = "Arial 16 bold").pack()

# Band 1
Gain1 = Scale(GUI, from_=6, to_=-30)
Gain1.pack(padx=5, pady=10, side=LEFT)
w = Label(GUI, text="BASS", bg="red", fg="white")
w.pack(padx=5, pady=10, side=LEFT)
#####infinite loop ( a must for GUI)
GUI.mainloop()



# Remove this later
mp.figure(1)
mp.subplot(211)
mp.plot(orig_audio)
mp.subplot(212)
mp.plot(output.astype("int16"))
mp.show()

# wv.write('lp_serato2.wav', audioFs, output.astype("int16"))

