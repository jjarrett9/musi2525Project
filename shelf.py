from __future__ import division
import math
import numpy as np 
import scipy.io.wavfile as wv
import wave
import sys
import contextlib

testAudioFs, testAudioSamples = wv.read('serato_bigband.wav')

audioOut = wave.open('audioOut', 'w')


choseFs = eval(input("input sample rate: "))
choseF0 = eval(input("input f0: "))

# only needed for shelving filters
slope = eval(input("input slope: "))
gain = eval(input("input gain: "))

# bandwidth in octaves 
bandwidth = eval(input("input bandwidth: "))

q = eval(input("input Q: "))



w0 = 2*math.pi*(choseF0/choseFs)


# A for shelfs
A = 10^(gain / 40)


cw0 = math.cos(w0)
sw0 = math.sin(w0)

# alpha for shelfs
alpha = (sw0 / 2) * math.sqrt((A + (1/A)) * ((1/slope) - 1) + 2)

# filter coefficients for low Shelf

b0 = A * ((A + 1) - (A - 1) * cw0 + 2 * math.sqrt(A) * alpha)
b1 = 2 * A * ((A - 1) - (A + 1) * cw0)
b2 = A * ((A + 1) - (A - 1) * cw0 - 2 * math.sqrt(A) * alpha)
a0 = (A + 1) + (A - 1) * cw0 + 2 * math.sqrt(A) * alpha
a1 = -2 * ((A - 1) + (A + 1) * cw0)
a2 = (A + 1) + (A - 1) * cw0 - 2 * math.sqrt(A) * alpha

# filter coefficients for high shelf 

b0 = A * ((A + 1) + (A - 1) * cw0 + 2 * math.sqrt(A) * alpha)
b1 = -2 * A * ((A - 1) + (A + 1) * cw0)
b2 = A * ((A + 1) + (A - 1) * cw0 - 2 * math.sqrt(A) * alpha)
a0 = (A + 1) - (A - 1) * cw0 + 2 * math.sqrt(A) * alpha
a1 = 2 * ((A - 1) - (A + 1) * cw0)
a2 = (A + 1) - (A - 1) * cw0 - 2 * math.sqrt(A) * alpha







# alpha for not shelfs
alpha = sw0/(2*q*A)



# filter coefficients for peaking (analog)
b0 = 10 ^ (gain / 20) * (1 + alpha * A)
b1 = 10 ^ (gain / 20) * (-2 * cw0)
b2 = 10 ^ (gain / 20) * (1 - alpha * A)
a0 = 1 + (alpha / A )
a1 = -2 * cw0
a2 = 1 - (alpha / A)

# normalize these so a0 = 1
b0 = b0 / a0
b1 = b1 / (2*a0)
b2 = b2 / a0
a1 = a1 / (-2 * a0)
a2 = a2 / -a0

maxB = max(abs(b0), abs(b1), abs(b2))

if maxB > 1:
    b0 = b0 / maxB
    b1 = b1 / maxB
    b2 = b2 / maxB

bits = 16 # may want to change later
rng = 2 ^ (bits - 1) - 1

# digital filter coefficients for peaking eq filter
n0 = math.floor(b0 * rng)
n1 = math.floor(b1 * rng)
n2 = math.floor(b2 * rng)
d1 = math.floor(a1 * rng)
d2 = math.floor(a2 * rng)