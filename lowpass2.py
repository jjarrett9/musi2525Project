from __future__ import division
import math
import numpy as np 
import scipy.io.wavfile as wv
import matplotlib.pyplot as mp


def filter (x, f0, fs, q):
    
    #initializing return array
    y = np.zeros(x.shape,x.dtype)
    
    w0 = 2*math.pi*(f0)
    tw0 = math.tan(w0/(2*fs))
    
    b0 = tw0
    b1 = tw0
    a0 = tw0 + 1
    a1 = tw0 - 1 
    
    #filter coefficients from trig wizardr
    
    #transfer functions
    for ch in range(0, x.shape[1]):
        for n in range(2,len(x)):
            y[n,ch] = (b0*x[n,ch] + b1*x[n-1,ch] - a1*y[n-1,ch])/a0
    
    return y


audioFs, orig_audio = wv.read('serato_bigband.wav')

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
wv.write('lowpassed_piano2.wav', audioFs, lp_audio)
mp.show()
