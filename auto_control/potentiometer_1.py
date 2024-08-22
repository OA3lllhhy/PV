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
import time
from pysmu import *
# define button actions
def Analog_in():
    global session, DevID, devx, loopnum, session
    while (True):       # Main loop
        if (RUNstatus.get() == 1):
            if not session.continuous:
                session.flush()
                session.start(0)
                #print "starting session inside analog in"
                time.sleep(0.02)
            DCVA = 0.0 # initalize measurment variable
            DCVB = 0.0 # initalize measurment variable
            ADsignal1 = devx.read(20, -1, True) # get 20 readings
            # get_samples returns a list of values for voltage [0] and current [1]
            for index in range(10): # calculate average
                DCVA += ADsignal1[index+10][0][0] # Sum for average CA voltage 
                DCVB  += ADsignal1[index+10][1][0] # Sum for average CB voltage
                # Sum for average voltage
            DCVA = DCVA / 10.0 # calculate average
            VAString = ' {0:.4f} '.format(DCVA) # format with 4 decimal places
            label.config(text = VAString) # change displayed value
            time.sleep(0.1)
            
    # Update tasks and screens by TKinter
        root.update_idletasks()
        root.update()            

# setup main window  
root = Tk()

label = Label(root, font = "Arial 16 bold")
label.grid(row=1, columnspan=1, sticky=W)
label.config(text = " ")
RUNstatus = IntVar(0)
rb1 = Radiobutton(root, text="Stop", variable=RUNstatus, value=0 )
rb1.grid(row=2, column=0, sticky=W)
rb2 = Radiobutton(root, text="Run", variable=RUNstatus, value=1 )
rb2.grid(row=2, column=1, sticky=W)
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
# Start sampling
Analog_in()
#
