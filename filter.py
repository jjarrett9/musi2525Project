import math
import numpy as np 
    
LOWPASS = 1
LOWSHELF = 2
BANDPASS = 3
PEAK = 4
NOTCH = 5
HIGHSHELF = 6
HIGHPASS = 7
    
class Filter:

    def __init__ (self):
        self.x1 = self.x2 = self.y1 = self.y2 = 0
    
    def filter (self, x, fs, band1, band2, band3):
    
        #initializing return array
        y = np.zeros(x.shape, x.dtype)
        
        
        lowCoeffs = self.getCoeffs(fs, band1)
        midCoeffs = self.getCoeffs(fs, band2)
        highCoeffs = self.getCoeffs(fs, band3)
        
        #transfer functions
        for ch in range(0, x.shape[1]):
            x1 = x2 = y1 = y2 = 0
            low1 = low2 = 0
            mid1 = mid2 = 0
            for n in range(0,len(x)): 
                
                low0 = np.matmul(lowCoeffs, [x[n,ch], x1, x2, low1, low2])
                mid0 = np.matmul(midCoeffs, [low0, low1, low2, mid1, mid2])
                y[n,ch] = np.matmul(highCoeffs, [mid0, mid1, mid2, y1, y2])
            
                x2 = x1
                x1 = x[n,ch]
                low2 = low1
                low1 = low0
                mid2 = mid1
                mid1 = mid0
                y2 = y1
                y1 = y[n,ch]
            
        return y
    
    def getCoeffs (self, fs, bandParams):
        type = bandParams[0]
        f0 = bandParams[1]
        q = bandParams[2]
        dBgain = bandParams[3]
        
        w = 2*math.pi*(f0/fs)
        cw = math.cos(w)
        sw = math.sin(w)
        alpha = sw/(2*q) 
        bigA  = 10 **(dBgain/40)
        
        #filter coefficients from trig wizardry
        
        b0 = b1 = b2 = a0 = a1 = a2 = 0 
        
        if type is LOWPASS:   
            
            b0 =  (1 - cw)/2
            b1 =   1 - cw
            b2 =  (1 - cw)/2
            a0 =   1 + alpha
            a1 =  -2*cw
            a2 =   1 - alpha 
            
        elif type is BANDPASS:
            
            b0 =  sw/2
            b1 =   0
            b2 =  sw/-2
            a0 =   1 + alpha
            a1 =  -2*cw
            a2 =   1 - alpha 
        
        elif type is NOTCH:
            
            b0 =  1
            b1 =   -2*cw
            b2 =  1
            a0 =   1 + alpha
            a1 =  -2*cw
            a2 =   1 - alpha 
        
        elif type is HIGHPASS:
            
            b0 =  (1 + cw)/2
            b1 =   -1*(1 + cw)
            b2 =  (1 + cw)/2
            a0 =   1 + alpha
            a1 =  -2*cw
            a2 =   1 - alpha 

        elif type is PEAK:

            b0 = 1 + alpha*bigA
            b1 = -2*cw
            b2 = 1-alpha*bigA
            a0 = 1 + alpha/bigA
            a1 = -2*cw
            a2 = 1-alpha/bigA

        elif type is LOWSHELF:

            b0 = bigA * ((bigA + 1) - (bigA - 1) * cw + 2 * math.sqrt(bigA)*alpha)
            b1 = 2 * bigA * ((bigA - 1) - (bigA + 1) * cw)
            b2 = bigA * ((bigA + 1) - (bigA - 1) * cw - 2*math.sqrt(bigA) * alpha)
            a0 = (bigA + 1) + (bigA - 1) * cw + 2 * math.sqrt(bigA) * alpha
            a1 = -2 * ((bigA - 1) + (bigA + 1) * cw)
            a2 = (bigA + 1) + (bigA - 1) * cw - 2*math.sqrt(bigA) * alpha

        elif type is HIGHSHELF:

            b0 = bigA * ((bigA + 1) + (bigA - 1) * cw + 2 * math.sqrt(bigA)*alpha)
            b1 = -2 * bigA * ((bigA - 1) + (bigA + 1) * cw)
            b2 = bigA * ((bigA + 1) + (bigA - 1) * cw - 2*math.sqrt(bigA) * alpha)
            a0 = (bigA + 1) - (bigA - 1) * cw + 2 * math.sqrt(bigA) * alpha
            a1 = 2 * ((bigA - 1) - (bigA + 1) * cw)
            a2 = (bigA + 1) - (bigA - 1) * cw - 2*math.sqrt (bigA) * alpha

        b0 /= a0
        b1 /= a0
        b2 /= a0
        a1 /= a0
        a2 /= a0
    
        return [b0, b1, b2, a1*-1, a2*-1]