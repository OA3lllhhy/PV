#!/usr/bin/python
#For Python version > = 2.7.8
import __future__
import sys
if sys.version_info[0] == 2:
    from Tkinter import *
if sys.version_info[0] == 3:
    from tkinter import *

import atexit
from collections import defaultdict
from operator import add
import math
import time
from pysmu import *
# Draw analog meter face
def Build_meter(Xcenter, Ycenter, Radius, Scale):

    ca.create_arc(Xcenter-Radius, Ycenter+Radius, Xcenter+Radius, Ycenter-Radius, start=315, extent=270, outline="black", fill="white", width=2)
    Tradius = 1.1 * Radius
    for tick in range(11):
        Angle = 225 - ((270*tick)/10)
        if Angle < 0.0:
            Angle = 360 - Angle
        RAngle = math.radians(Angle)
        y = Tradius*math.sin(RAngle)
        x = Tradius*math.cos(RAngle)
        if Angle > 270:
            y = 0 - y
        Increment = 10/Scale
        axis_value = float(tick/Increment)
        axis_label = str(axis_value)
        ca.create_text(Xcenter+x,Ycenter-y, text = axis_label)
    
    return(ca.create_line(Xcenter, Ycenter, Xcenter+10, Ycenter+10, fill="red", width=3))

# define button actions
def Analog_in(Xcenter, Ycenter, Radius, Scale):
    global session, DevID, devx, loopnum
    global Indicator
    while (True):       # Main loop
        if (RUNstatus.get() == 1):
            if not session.continuous:
                session.flush()
                session.start(0)
                #print "starting session inside analog in"
                time.sleep(0.02)
            DCVA = 0.0 # initalize measurment variable
            ADsignal1 = devx.read(20, -1, True) # get 20 readings
            # get_samples returns a list of values for voltage [0] and current [1]
            for index in range(10): # calculate average
                SPA = ADsignal1[index+10][0][0] # skip over first 10 readings
                VAdata = float(SPA)
                DCVA += VAdata # Sum for average voltage
            DCVA = DCVA / 10.0 # calculate average
            VAString = ' {0:.4f} '.format(DCVA) # format with 4 decimal places
            label.config(text = VAString) # change displayed value
            Angle = 225 - ((270*DCVA)/Scale)
            if Angle < 0.0:
                Angle = 360 - Angle
            RAngle = math.radians(Angle)
            y = 110*math.sin(RAngle)
            x = 110*math.cos(RAngle)
            if Angle > 270:
                y = 0 - y
            ca.delete(Indicator)
            Indicator = ca.create_line(Xcenter, Ycenter, Xcenter+x, Ycenter-y, fill="red", width=3)
            time.sleep(0.1)
            
    # Update tasks and screens by TKinter
        root.update_idletasks()
        root.update()            

# setup main window  
root = Tk()

#
label = Label(root, font = "Arial 16 bold")
label.grid(row=1, columnspan=1, sticky=W)
label.config(text = " ")
RUNstatus = IntVar(0)
rb1 = Radiobutton(root, text="Stop", variable=RUNstatus, value=0 )
rb1.grid(row=2, column=0, sticky=W)
rb2 = Radiobutton(root, text="Run", variable=RUNstatus, value=1 )
rb2.grid(row=2, column=1, sticky=W)
#
ca = Canvas(root, width=300, height=300, background="white")
ca.grid(row=3, column=0, columnspan=4, sticky=W)

# Setup ADAML1000
session = Session(ignore_dataflow=True, queue_size=10000)
if not session.devices:
    print( 'no device found')
    root.destroy()
    exit()
#
devx = session.devices[0]
CHA = devx.channels['A']    # Open CHA
CHA.mode = Mode.HI_Z # Put CHA in Hi Z mode
CHB = devx.channels['B']    # Open CHB
CHB.mode = Mode.HI_Z # Put CHB in Hi Z mode
ADsignal1 = []
# start main loop
root.update()
Indicator = Build_meter(150, 150 , 100, 5.0)
# Start sampling
Analog_in(150, 150 , 100, 5.0)
#
