from __future__ import division
import math
import numpy as np 
import scipy.io.wavfile as wv
import matplotlib.pyplot as mp
import time
import filter


def generateRandomNoise(t):
    t *= 44100
    t = int(t)
    noise = np.random.normal(0,10000,(t,2))
    
    return noise 

audioFs, orig_audio = wv.read('serato_bigband.wav')

f0 = eval(input("Enter center frequency: "))
q = eval(input("Enter filter Q: "))
g = eval(input("Enter gain: "))
print("Working...")
start = time.time()
f = filter.Filter()
lp_audio = f.filterWav(orig_audio*1., f0, audioFs, q, filter.Filter.NOTCH)
output = np.clip(lp_audio, -32767, 32768)

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
wv.write('lp_serato2.wav', audioFs, output.astype("int16"))

