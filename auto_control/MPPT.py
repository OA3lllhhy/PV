from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import pysmu
from pysmu import Session, Mode
from scipy.optimize import curve_fit
from scipy.optimize import minimize_scalar
from scipy.optimize import fsolve
from signal import signal, SIG_DFL, SIGINT

if sys.stdout.isatty():
    output = lambda s: sys.stdout.write("\r" + s)
else:
    output = print

if __name__ == '__main__':

    signal = signal(SIGINT, SIG_DFL)

    session = Session()

    voltage_step = 0.015
    last_power = 0
    voltage = 0.5

    voltages = []
    currents = []
    powers = []
    # powers = np.array(powers)
    time_start = time.time()

    if session.devices:
        dev = session.devices[0]

        chan_a = dev.channels['A']
        chan_b = dev.channels['B']
        chan_a.mode = Mode.SVMI
        chan_b.mode = Mode.HI_Z

        session.start(1)
        print("Program running")
        for _ in range(500):
            try:
                chan_a.constant(voltage)
                session.read(1)

                samples = dev.get_samples(1)
                for x in samples:
                    current = x[0][1]
                    power = voltage * current

                if power > last_power:
                    voltage += voltage_step
                else:
                    voltage_step = - voltage_step
                    voltage += voltage_step
                last_power = power

                voltages.append(voltage)
                currents.append(current)
                powers.append(power)
            except pysmu.exceptions.WriteTimeout as e:
                print("Runtime error, retrying")
                time.sleep(0.5)
            
            time.sleep(0.1)
        
        session.end()

    else:
        print("No device found")
        sys.exit(1)

    for i in range(len(powers)):
        powers[i] = - powers[i]


    def power_curve(voltage, a, b, c):
        return (a - b * np.exp(-c * voltage)) * voltage
    
    # Extract the data in the interval [0, 0.6]

    voltage_fit = []
    power_fit = []
    for i in range(len(voltages)):
        if voltages[i] > 0:
            voltage_fit.append(voltages[i])
            power_fit.append(powers[i])

    initial_guess = [3, 3, 0]
    params, covariance = curve_fit(power_curve, voltage_fit, power_fit, p0=initial_guess, maxfev=10000)
    errors = np.sqrt(np.diag(covariance))
    print(f"Number of fitting data points: {len(voltage_fit)}")
    print(f"Fitted parameters: a = {params[0]:.3f} +/- {errors[0]:.3f}")
    print(f"Fitted parameters: b = {params[1]:.3f} +/- {errors[1]:.3f}")
    print(f"Fitted parameters: c = {params[2]:.3f} +/- {errors[2]:.3f}")

    def negative_power_curve(voltage):
        return - power_curve(voltage, *params)
    
    result = minimize_scalar(negative_power_curve, bounds=(0, 0.6), method='bounded')
    mpp_voltage = result.x
    mpp_power = power_curve(mpp_voltage, *params)
    print("Maximum Power Point: Voltage = {:.3f} V, Power = {:.3f} W".format(mpp_voltage, mpp_power))

    time_end = time.time()
    print("Execution time: {:.2f} s".format(time_end - time_start))

    x = np.linspace(0, 0.6, 100)
    plt.scatter(voltage_fit, power_fit, s = 10,label='Measured Power')
    plt.plot(x, power_curve(x, *params), color = 'red',label='Fitted Power Curve')
    plt.scatter([mpp_voltage], [mpp_power], color='yellow', s=100, label='MPP')
    plt.title('Voltage-Power Curve')
    plt.xlabel('Voltage (V)')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 0.6)
    plt.ylim(0, 0.015)
    plt.show()