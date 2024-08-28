"""
This python script control the ADALM-1000 with triangle wave voltage input
and measure the current output of the solar cell and hence plot the IV curve
and PV curve of the cell. Also, calculates the V_oc, I_sc, V_mp, I_mp and
fill factor of the cell.
"""
from __future__ import print_function
from signal import signal, SIG_DFL, SIGINT
from scipy.signal import savgol_filter
import random
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import curve_fit
from scipy.optimize import minimize_scalar
from pysmu import Session, Mode

if sys.stdout.isatty():
    output = lambda s: sys.stdout.write("\r" + s)
else:
    output = print

if __name__ == '__main__':
    signal(SIGINT, SIG_DFL)
    session = Session()

    if session.devices:    
        dev = session.devices[0]
        dev.ignore_dataflow = sys.stdout.isatty()

        chan_a = dev.channels['A']
        chan_b = dev.channels['B']

        # set channel to source voltage, measure current mode
        chan_a.mode = Mode.SVMI
        chan_b.mode = Mode.HI_Z

        # set channel to triangle wave with 0.8V amplitude, 0 offset, 10Hz frequency, 0 phase
        chan_a.triangle(0.8, 0, 10, 0)

        # start a continous session with 1000 samples store all the data in a dataframe
        start_time = time.time()
        session.start(0)
        voltage_data = []
        current_data = []

        # Run the session in continuous mode for 10 seconds
        while time.time() - start_time < 10:
            samples = dev.get_samples(1000) # get 1000 samples
            for x in samples:
                voltage_data.append(x[0][0])
                current_data.append(x[0][1])

        if current_data is not None:
            length = len(voltage_data)
            x = np.linspace(0, length, length)
            voltage_data = np.array(voltage_data)
            current_data = np.array(current_data)
            
            # Extract the data in the interval [0, 0.6]
            min = 0
            max = 0.6
            mask = (voltage_data >= min) & (voltage_data <= max)
            voltage_fit = voltage_data[mask]
            current_fit = current_data[mask]

            # Fit the IV curve
            def fit_func(x, a, b, c):
                return a - b * np.exp(c * x)
            
            initial_guess = [0.1, 2e-11, 38]
            popt, pcov = curve_fit(fit_func, voltage_fit, -current_fit, p0=initial_guess)
            # print("a = ", popt[0], "b = ", popt[1], "c = ", popt[2])

            # calculate the R^2 value
            residuals = -current_fit - fit_func(voltage_fit, *popt)
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((current_fit - np.mean(current_fit))**2)
            r_squared = 1 - (ss_res / ss_tot)
            print("R^2 = ", r_squared)

            x = np.linspace(0, 0.7, 100)

            # finding V_oc, I_sc, V_mp and I_mp (to shade the region on the graph)
            def negative_PV(x):
                return - fit_func(x, *popt) * x
            
            def IV(x):
                return fit_func(x, *popt)
            
            I_sc = fit_func(0, *popt) # short circuit current
            V_op = fsolve(IV, 0.55) # open circuit voltage

            # print("V_op: ", V_op[0], "I_sc: ", I_sc, )

            result = minimize_scalar(negative_PV, bounds=(0,0.6))
            V_mp = result.x
            I_mp = fit_func(V_mp, *popt) * V_mp
            # print("V_mp: ", V_mp, "I_mp: ", I_mp)

            ff = (V_mp * I_mp) / (I_sc * V_op[0])
            # print("Fill Factor: ", ff)

            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1.plot(voltage_fit, -current_fit, '.', color = 'blue',label='IV curve')
            ax2.plot(voltage_fit, -current_fit * voltage_fit, '.', color = 'orange',label='PV curve')
            # ax1.plot(x, fit_func(x, *popt), color = 'red')
            # ax2.plot(x, fit_func(x, *popt) * x, color = 'green')
        ax1.set_xlabel('Voltage (V)')
        ax1.set_ylabel('Current (A)')
        ax2.set_ylabel('Power (W)')
        ax1.set_xlim(0, 0.6)
        ax1.set_ylim(0, 0.15)
        ax2.set_ylim(0, 0.15)
        ax1.set_title('IV and PV curve')
        ax1.grid(True)
        ax1.legend(loc='upper right')
        ax2.legend(loc='upper left')
        plt.show()

        session.end()
            
    else:
        print('no devices attached')