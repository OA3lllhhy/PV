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
        chan_b.mode = Mode.SVMI

        # set channel to triangle wave with 1V amplitude, 0 offset, 10Hz frequency, 0 phase
        chan_a.triangle(0.8, 0, 1000, 0)
        chan_b.triangle(1, 0, 30, 0)

        # start a continous session with 1000 samples store all the data in a dataframe
        start_time = time.time()
        session.start(1000)
        voltage_data = []
        current_data = []
        count = 0

        # Run the session in continuous mode for 2 seconds
        while time.time() - start_time < 10:
            samples = dev.get_samples(1000)
            for x in samples:
                voltage_data.append(x[0][0])
                current_data.append(x[0][1])
                count += 1
                # output("{: 6f} {: 6f}".format(x[0][0], x[1][0]))

        # stop the session
        print("count: ", count)
        # print(voltage_data)

        # Plot the data
        length = len(voltage_data)
        x = np.linspace(0, length, length)
        voltage_data = np.array(voltage_data)
        current_data = np.array(current_data)

        # Apply a Savitzky-Golay filter to the data
        # voltage_data = savgol_filter(voltage_data, 51, 3)
        # current_data = savgol_filter(current_data, 51, 3)

        if current_data is not None:

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
            print("a = ", popt[0], "b = ", popt[1], "c = ", popt[2])

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
            
            I_sc = fit_func(0, *popt)
            V_op = fsolve(IV, 0.55)

            print("V_op: ", V_op[0], "I_sc: ", I_sc, )

            result = minimize_scalar(negative_PV, bounds=(0,0.6))
            V_mp = result.x
            I_mp = fit_func(V_mp, *popt) * V_mp
            print("V_mp: ", V_mp, "I_mp: ", I_mp)

            ff = (V_mp * I_mp) / (I_sc * V_op[0])
            print("Fill Factor: ", ff)

            #plt.plot(voltage_fit, -current_fit, '.')
            #plt.plot(voltage_fit, - current_fit * voltage_fit, '.')
            plt.plot(x, fit_func(x, *popt), label='IV curve fit')
            plt.plot(x, fit_func(x, *popt) * x, label='PV curve fit')
        plt.xlim(0, 0.6)
        plt.ylim(0, 0.15)
        plt.grid()
        plt.show()


        session.end()
        
        
            
    else:
        print('no devices attached')