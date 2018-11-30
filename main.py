from __future__ import division
import math
import numpy as np 
import scipy.io.wavfile as wv
import matplotlib.pyplot as mp
import time
import filter
import simpleaudio as sa

f = filter.Filter()

def generateRandomNoise(t):
    t = int(t)
    noise = np.random.normal(0,10000,(t,2))
    return noise; 

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
filtered = f.filter(orig_audio*1., audioFs, f0, q, filter.Filter.LOWPASS)
output = np.clip(filtered, -32767, 32768)
end = time.time() - start
print("Done.")

length = len(orig_audio)
print(f"{end*audioFs:.0f} samples ({end:.3f} seconds) elapsed, processed {length:d} samples ({length/audioFs:.3f} seconds).")

wave_obj = sa.WaveObject(output.astype("int16"), 2, 2, 44100)
play_obj = wave_obj.play()


# Remove this later
mp.figure(1)
mp.subplot(211)
mp.plot(orig_audio)
mp.subplot(212)
mp.plot(output.astype("int16"))
mp.show()

wv.write('lp_serato2.wav', audioFs, output.astype("int16"))

