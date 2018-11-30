import math
import numpy as np 
class Filter:
    LOWPASS = 1
    LOWSHELF = 2
    BANDPASS = 3
    PEAK = 4
    NOTCH = 5
    HIGHSHELF = 6
    HIGHPASS = 7

    def __init__ (self):
        self.x1 = self.x2 = self.y1 = self.y2 = 0
    
    def reset(self):
        self.x1 = self.x2 = self.y1 = self.y2 = 0
    
    def filterWav (self, x, f0, fs, q, type):
    
        #initializing return array
        y = np.zeros(x.shape, x.dtype)
        
        coeffs = self.getCoeffs(f0, fs, q, type)
        
        #transfer functions
        for ch in range(0, x.shape[1]):
            for n in range(0,len(x)):
                samples = [x[n,ch], self.x1, self.x2, self.y1, self.y2]
                y[n,ch] = np.matmul(coeffs, samples)
            
                self.x2 = self.x1
                self.x1 = x[n,ch]
                self.y2 = self.y1
                self.y1 = y[n,ch]
            
            self.reset()
        return y
    
    def getCoeffs (self, f0, fs, q, type):
        w = 2*math.pi*(f0/fs)
        cw = math.cos(w)
        sw = math.sin(w)
        alpha = sw/(2*q) 
    
        #filter coefficients from trig wizardry
        
        b0 = b1 = b2 = a0 = a1 = a2 = 0 
        
        if type is Filter.LOWPASS:   
            
            b0 =  (1 - cw)/2
            b1 =   1 - cw
            b2 =  (1 - cw)/2
            a0 =   1 + alpha
            a1 =  -2*cw
            a2 =   1 - alpha 
            
        elif type is Filter.BANDPASS:
            
            b0 =  sw/2
            b1 =   0
            b2 =  sw/-2
            a0 =   1 + alpha
            a1 =  -2*cw
            a2 =   1 - alpha 
        
        elif type is Filter.NOTCH:
            
            b0 =  1
            b1 =   -2*cw
            b2 =  1
            a0 =   1 + alpha
            a1 =  -2*cw
            a2 =   1 - alpha 
        
    
        elif type is Filter.HIGHPASS:
            
            b0 =  (1 + cw)/2
            b1 =   -1*(1 + cw)
            b2 =  (1 + cw)/2
            a0 =   1 + alpha
            a1 =  -2*cw
            a2 =   1 - alpha 
    
        b0 /= a0
        b1 /= a0
        b2 /= a0
        a1 /= a0
        a2 /= a0
    
        return [b0, b1, b2, a1*-1, a2*-1]