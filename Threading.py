from tkinter import *
import math
import pyaudio
import wave
import struct
import threading
import scipy as sp 
from scipy import signal

from myfunctions import clip16

#####Making variables global to switch between class and function#####
gain1 = 0 
gain2 = 0
gain3 = 0
Qpass = 10
f1pass= 500
f2pass= 10000
f3pass= 20000

####Slider values are passed to filter########
def getvalue_1():
        global gain1
        return gain1
def getvalue_2():
        global gain2
        return gain2
def getvalue_3():
        global gain3
        return gain3
def getQ():
        global Qpass
        return Qpass
def getf1():
        global f1pass
        return f1pass
def getf2():
        global f2pass
        return f2pass
def getf3():
        global f3pass
        return f3pass



      
########## Slider values are read ############
def update_values_1(event):
  global gain1
  gain1=scale1.get()
def update_values_2(event):
  global gain2
  gain2=scale2.get()
def update_values_3(event):
  global gain3
  gain3=scale3.get()
def updateQ():
  global Qpass
  Qpass = float(e.get())
def updatef1():
  global f1pass
  f1pass = float(f1.get())
def updatef2():
  global f2pass
  f2pass = float(f2.get())  
def updatef3():
  global f3pass
  f3pass = float(f3.get())        
  
#########Class Function Initialisation#############  
class main():
  def __init__(self):

        # Import audio file
        importedFile = 'auth_mono_large.wav'

        print("Play the wave file %s." % importedFile)
        # Open and read wave file (should be mono channel)
        self.wf = wave.open( importedFile, 'rb' )
        # properties
        self.num_channels = self.wf.getnchannels()       	# mono or stereo
        self.RATE = self.wf.getframerate()                      # fs
        self.signal_length  = self.wf.getnframes()       	# Signal length
        self.width = self.wf.getsampwidth()       		# Number of bytes per sample
        print("The file has %d channel(s)." % self.num_channels)
        print("The sample rate is %d." % self.RATE)
        print("The file has %d samples." % self.signal_length)
        print("There are %d bytes per sample." % self.width)

   ########  Difference equation coefficients for Low Shelving filters   #########
        self.fc_l = 0     # default to 0
        self.dbGain_l = 0
        self.Q = 2
        self.w_l = 2*math.pi*(self.fc_l/self.RATE)
        cwl = math.cos(self.w_l)
        swl = math.sin(self.w_l)
        self.alpha = swl/(2*self.Q)
        self.bigA_low = 10**(self.dbGain_l/40)


        self.b0 = self.bigA_low * ((self.bigA_low + 1) + (self.bigA_low - 1) * cwl + 2 * math.sqrt(self.bigA_low)*self.alpha)
        self.b1 = 2 * self.bigA_low * ((self.bigA_low - 1) - (self.bigA_low + 1) * cwl)
        self.b2 = self.bigA_low * ((self.bigA_low + 1) - (self.bigA_low - 1) * cwl - 2*math.sqrt(self.bigA_low) * self.alpha)
        self.a0 = (self.bigA_low + 1) + (self.bigA_low - 1) * cwl + 2 * math.sqrt(self.bigA_low) * self.alpha
        self.a1 = -2 * ((self.bigA_low - 1) + (self.bigA_low + 1) * cwl)
        self.a2 = (self.bigA_low + 1) + (self.bigA_low - 1) * cwl - 2*math.sqrt(self.bigA_low) * self.alpha
        
   ########  Difference equation coefficients for high shelving filter   ######
        self.fc_h = 0     # default to 0
        self.dbGain_h = 0
        self.Q = 2
        self.w_h = 2*math.pi*(self.fc_h/self.RATE)
        cwh = math.cos(self.w_h)
        swh = math.sin(self.w_h)
        self.alpha_h = swh/(2*self.Q)
        self.bigA_high = 10**(self.dbGain_h/40)
        
        self.b3 = self.bigA_high * ((self.bigA_high + 1) + (self.bigA_high - 1) * cwh + 2 * math.sqrt(self.bigA_high)*self.alpha_h)
        self.b4 = -2 * self.bigA_high * ((self.bigA_high - 1) + (self.bigA_high + 1) * cwh)
        self.b5 = self.bigA_high * ((self.bigA_high + 1) - (self.bigA_high - 1) * cwh - 2*math.sqrt(self.bigA_high) * self.alpha_h)
        self.a3 = (self.bigA_high + 1) - (self.bigA_high - 1) * cwh + 2 * math.sqrt(self.bigA_high) * self.alpha_h
        self.a4 = 2 * ((self.bigA_high - 1) - (self.bigA_high + 1) * cwh)
        self.a5 = (self.bigA_high + 1) - (self.bigA_high - 1) * cwh - 2*math.sqrt (self.bigA_high) * self.alpha_h

   ################ Difference equation for Peak filter ################
        self.fc_p = 0     # default to 0
        self.dbGain_p = 0
        self.Q = 2
        self.w_p = 2*math.pi*(self.fc_p/self.RATE)
        cwp = math.cos(self.w_p)
        swp = math.sin(self.w_p)
        self.alpha_p = swp/(2*self.Q)
        self.bigA_peak = 10**(self.dbGain_p/40)      

        self.b6 = 1 + self.alpha_p*self.bigA_peak
        self.b7 = -2*cwp
        self.b8 = 1-self.alpha_p*self.bigA_peak
        self.a6 = 1 + self.alpha_p/self.bigA_peak
        self.a7 = -2*cwp
        self.a8 = 1-self.alpha_p/self.bigA_peak


################################################################
  def Pythread(self):
        # Open audio stream
        p = pyaudio.PyAudio()
        stream = p.open(format      = pyaudio.paInt16,
                channels    = self.num_channels,
                rate        = self.RATE,
                input       = False,
                output      = True )

        BLOCKSIZE = 1024
        
        # Create block (initialize to zero)
        output_block = [0 for n in range(0, BLOCKSIZE)]
        self.y1 = [0 for n in range(0, BLOCKSIZE)]
        self.y2 = [0 for n in range(0, BLOCKSIZE)]
        self.y3 = [0 for n in range(0, BLOCKSIZE)]
        x = [0 for n in range(0, BLOCKSIZE)]
        
        # Number of blocks in wave file
        
        num_blocks = int(math.floor(self.signal_length/BLOCKSIZE))

        
        self.a0 = 1
                
        self.b_l = [self.b0, self.b1, self.b2]
        self.a_l = [self.a0, self.a1, self.a2]

        self.b_h = [self.b3, self.b4, self.b5]
        self.a_h = [self.a3 ,self.a4, self.a5]

        self.b_p = [self.b6 ,self.b7, self.b8]
        self.a_p = [self.a6, self.a7 ,self.a8]

        
        for i in range(0, num_blocks):

                input_string = self.wf.readframes(BLOCKSIZE)
                input_tuple = struct.unpack('h' * BLOCKSIZE , input_string)  # One-element tuple
                x=input_tuple
                
                self.y1 = sp.signal.lfilter(self.b_l,self.a_l,x)        #LP
                self.y2 = sp.signal.lfilter(self.b_h,self.a_h,self.y1)        #HP
                self.y3 = sp.signal.lfilter(self.b_p,self.a_p,self.y2)        #PF

                output_value = self.y3

                
 
                
                #sys.exit(0)
                               
                # Compute output value
                output_value = clip16(output_value)    # Number
                # Convert output value to binary string
                output_string = struct.pack('h'*BLOCKSIZE, *output_value.astype("int16"))
                
                # Write binary string to audio stream
                stream.write(output_string)                                

                ################################# Low pass  ###################################
                self.fc_l = getf1()     # default to 0
                self.w_l = 2*math.pi*(self.fc_l/self.RATE)
                cwl = math.cos(self.w_l)
                swl = math.sin(self.w_l)
                self.Q = getQ()
                self.alpha = swl/(2*self.Q)
                self.bigA_low = 10**(self.dbGain_l/40)


                self.b0 = self.bigA_low * ((self.bigA_low + 1) + (self.bigA_low - 1) * cwl + 2 * math.sqrt(self.bigA_low)*self.alpha)
                self.b1 = 2 * self.bigA_low * ((self.bigA_low - 1) - (self.bigA_low + 1) * cwl)
                self.b2 = self.bigA_low * ((self.bigA_low + 1) - (self.bigA_low - 1) * cwl - 2*math.sqrt(self.bigA_low) * self.alpha)
                self.a0 = (self.bigA_low + 1) + (self.bigA_low - 1) * cwl + 2 * math.sqrt(self.bigA_low) * self.alpha
                self.a1 = -2 * ((self.bigA_low - 1) + (self.bigA_low + 1) * cwl)
                self.a2 = (self.bigA_low + 1) + (self.bigA_low - 1) * cwl - 2*math.sqrt(self.bigA_low) * self.alpha
                

                ###############################  High pass   ##################################
                self.fc_h = getf3()	#cut odd frequency for high shelving filter  
                self.w_h = 2*math.pi*(self.fc_h/self.RATE)
                cwh = math.cos(self.w_h)
                swh = math.sin(self.w_h)
                self.Q = getQ()
                self.alpha_h = swh/(2*self.Q)
                self.bigA_high = 10**(self.dbGain_h/40)
                
                self.b3 = self.bigA_high * ((self.bigA_high + 1) + (self.bigA_high - 1) * cwh + 2 * math.sqrt(self.bigA_high)*self.alpha_h)
                self.b4 = -2 * self.bigA_high * ((self.bigA_high - 1) + (self.bigA_high + 1) * cwh)
                self.b5 = self.bigA_high * ((self.bigA_high + 1) - (self.bigA_high - 1) * cwh - 2*math.sqrt(self.bigA_high) * self.alpha_h)
                self.a3 = (self.bigA_high + 1) - (self.bigA_high - 1) * cwh + 2 * math.sqrt(self.bigA_high) * self.alpha_h
                self.a4 = 2 * ((self.bigA_high - 1) - (self.bigA_high + 1) * cwh)
                self.a5 = (self.bigA_high + 1) - (self.bigA_high - 1) * cwh - 2*math.sqrt (self.bigA_high) * self.alpha_h


                ############################### Peak filter   #################################
                self.fc_p = getf2()                 
                self.w_p = 2*math.pi*(self.fc_p/self.RATE)
                cwp = math.cos(self.w_p)
                swp = math.sin(self.w_p)
                self.Q = getQ()
                self.alpha_p = swp/(2*self.Q)
                self.bigA_peak = 10**(self.dbGain_p/40)      

                self.b6 = 1 + self.alpha_p*self.bigA_peak
                self.b7 = -2*cwp
                self.b8 = 1-self.alpha_p*self.bigA_peak
                self.a6 = 1 + self.alpha_p/self.bigA_peak
                self.a7 = -2*cwp
                self.a8 = 1-self.alpha_p/self.bigA_peak

                #print self.b7
                #sys.exit(0)
                        

                self.b_l = [self.b0, self.b1, self.b2]
                self.a_l = [self.a0, self.a1, self.a2]

                self.b_h = [self.b3, self.b4, self.b5]
                self.a_h = [self.a3 ,self.a4, self.a5]

                self.b_p = [self.b6 ,self.b7, self.b8]
                self.a_p = [self.a6, self.a7 ,self.a8]

                               
                ######  Update values of gain fetched from the slider   ######
                self.dbGain = getvalue_1()
                self.dbGain_h = getvalue_3()
                self.dbGain_p = getvalue_2()
                ################
                ##print self.fc
                #print self.fc_h
                #print self.fc_p

        print("**** Done ****")
        stream.stop_stream()
        
        stream.close()
        p.terminate()
        

def RESET_RESPONSE():
    scale1.set(0)    
    scale2.set(0)
    scale3.set(0)

def FLAT_RESPONSE():
    scale1.set(10)    
    scale2.set(10)
    scale3.set(10)

def JAZZ_RESPONSE():
    scale1.set(22)    
    scale2.set(13)
    scale3.set(19)

def ROCK_RESPONSE():
    scale1.set(31)    
    scale2.set(18)
    scale3.set(23)    

##########Thread############
a = main()
thread = threading.Thread(target=a.Pythread) #Thread for object "a" of class Thread
thread.daemon = True 
thread.start()

###### GUI ########
GUI = Tk()
### GOEMETRY of the Window dialog box
GUI.geometry("600x400+300+300")
GUI.configure(background='brown')

Label(GUI, 
		 text="PARAMETRIC MUSIC EQUALISER",
		 fg = "white",
		 bg = "black",
		 font = "Helvetica 16 bold ").pack()

###slider 1
scale1 = Scale( GUI, from_=0, to_=50 ,command=update_values_1 )
scale1.pack(padx=5, pady=10, side=LEFT)
w = Label(GUI, text="BASS", bg="red", fg="white")
w.pack(padx=5, pady=10, side=LEFT)
###slider 2
scale2 = Scale( GUI, from_=0, to=50,command=update_values_2  )
scale2.pack(padx=5, pady=20, side=LEFT)
w = Label(GUI, text="MIDS", bg="green", fg="black")
w.pack(padx=5, pady=20, side=LEFT)
### slider 3
scale3 = Scale( GUI, from_=0, to=50 ,command=update_values_3 )
scale3.pack(padx=5, pady=20, side=LEFT)
w = Label(GUI, text="TREBLE", bg="blue", fg="white")
w.pack(padx=5, pady=20, side=LEFT)
### BUTTON-ENTRY Q
e = Entry(GUI)
e.pack()
#e.insert(0, 1)
b = Button(GUI, text="Enter Q factor", width=10, command = updateQ )
b.pack()

### BUTTON-ENTRY f1
f1 = Entry(GUI)
f1.pack()
#e.insert(0, 1)
b1 = Button(GUI, text="LOW_FREQ", width=10, command = updatef1 )
b1.pack()

### BUTTON-ENTRY f2
f2 = Entry(GUI)
f2.pack()
#e.insert(0, 1)
b2 = Button(GUI, text="MID_FREQ", width=10, command = updatef2 )
b2.pack()

### BUTTON-ENTRY f3
f3 = Entry(GUI)
f3.pack()
#e.insert(0, 1)
b2 = Button(GUI, text="HIGH_FREQ", width=10, command = updatef3 )
b2.pack()



button1 = Button( GUI, text='RESET',width=100, command = RESET_RESPONSE)
button1.pack()
button2 = Button( GUI, text='JAZZ',width=100, command = JAZZ_RESPONSE)
button2.pack()
button3 = Button( GUI, text='ROCK',width=100, command = ROCK_RESPONSE)
button3.pack()
button4 = Button( GUI, text='FLAT',width=100, command = FLAT_RESPONSE)
button4.pack()


#####infinite loop ( a must for GUI)
GUI.mainloop()
