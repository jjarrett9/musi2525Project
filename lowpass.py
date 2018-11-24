from __future__ import division
import math
import numpy as np 
import scipy.io.wavfile as wv
import matplotlib.pyplot as mp
import time

def filter (x, f0, fs, q):
    
    #initializing return array
    x1 = x2 = y1 = y2 = 0
    y = np.zeros(x.shape, x.dtype)
    
    w = 2*math.pi*(f0/fs)
    cw = math.cos(w)
    sw = math.sin(w)
    
    alpha = sw/(2*q) 
    
    #filter coefficients from trig wizardry
    
    b0 =  (1 - cw)/2
    b1 =   1 - cw
    b2 =  (1 - cw)/2
    a0 =   1 + alpha
    a1 =  -2*cw
    a2 =   1 - alpha 
    
    b0 /= a0
    b1 /= a0
    b2 /= a0
    a1 /= a0
    a2 /= a0
    
    coeffs = [b0, b1, b2, a1*-1, a2*-1]
    
    #transfer functions
    for ch in range(0, x.shape[1]):
        for n in range(0,len(x)):
            samples = [x[n,ch], x1, x2, y1, y2]
            y[n,ch] = np.matmul(coeffs, samples)
            
            x2 = x1
            x1 = x[n,ch]
            y2 = y1
            y1 = y[n,ch]
        
    return yy


def generateRandomNoise(t):
    t *= 44100
    t = int(t)
    noise = np.random.normal(0,10000,(t,2))
    
    return noise 

audioFs, orig_audio = wv.read('serato_bigband.wav')

f0 = eval(input("Enter center frequency: "))
q = eval(input("Enter filter Q: "))
print("Working...")
start = time.time()
lp_audio = filter(orig_audio, f0, audioFs, q)
#n = generateRandomNoise(28)
mp.figure(1)
mp.subplot(211)
#mp.plot(n)
mp.plot(orig_audio)

# lp_audio = filter(n, f0, 44100, q)
mp.subplot(212)
mp.plot(lp_audio)
end = time.time() - start
print(end)
print("Done.")
mp.show()
wv.write('lp_serato.wav', audioFs, lp_audio)

