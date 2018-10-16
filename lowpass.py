from __future__ import division
import math
import numpy as np 
import scipy.io.wavfile as wv
import matplotlib.pyplot as mp
import wave
import sys
import contextlib

def filter (x, f0, fs, q):
    
    #initializing return array
    y = np.zeros((len(x),2),x.dtype)
    
    w0 = 2*math.pi*(f0/fs)
    cw0 = math.cos(w0)
    sw0 = math.sin(w0)
    
    alpha = sw0/(2*q) 
    
    #filter coefficients from trig wizardry
    b0 =  (1 - cw0)/2
    b1 =   1 - cw0
    b2 =  (1 - cw0)/2
    a0 =   1 + alpha
    a1 =  -2*cw0
    a2 =   1 - alpha 
    
    #transfer functions
    for n in range(2,len(x)):
        
        y[n,0] = (b0*x[n,0] + b1*x[n-1,0] + b2*x[n-2,0] - a1*y[n-1,0] - a2*y[n-2,0])/a0
        y[n,1] = (b0*x[n,1] + b1*x[n-1,1] + b2*x[n-2,1] - a1*y[n-1,1] - a2*y[n-2,1])/a0 
    
    return y


audioFs, orig_audio = wv.read('piano_2.wav')

f0 = eval(input("Enter center frequency: "))
q = eval(input("Enter filter Q: "))
print("Working...")
lp_audio = filter(orig_audio, f0, audioFs, q)

mp.figure(1)
mp.subplot(211)
mp.plot(orig_audio[48000:52800])
mp.subplot(212)
mp.plot(lp_audio[48000:52800])
print("Done.")
wv.write('lowpassed_piano.wav', audioFs, lp_audio)
mp.show()
