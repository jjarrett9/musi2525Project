from __future__ import division
import math
import numpy as np 
import wave
import sys
import contextlib

choseFs = eval(input("input sample rate: "))
choseF0 = eval(input("input f0: "))
gain = eval(input("input gain: "))
slope = eval(input("input slope: "))

w0 = 2*math.pi*(choseF0/choseFs)

A = 10^(gain/40)

cw0 = math.cos(w0)
sw0 = math.sin(w0)

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
