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

    voltage_step = 0.02
    last_power = 0
    voltage = 0.5

    voltages = []
    currents = []
    powers = []
    # powers = np.array(powers)

    if session.devices:
        dev = session.devices[0]

        chan_a = dev.channels['A']
        chan_b = dev.channels['B']
        chan_a.mode = Mode.SVMI
        chan_b.mode = Mode.HI_Z

        session.start(100)
        
        for _ in range(100):
            try:
                chan_a.constant(voltage)
                session.read(0)
                # current = chan_a.current
                # power = voltage * current

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
    # powers = np.array(powers)
    # plt.plot(voltages, - powers, '.')
    # plt.xlim(0, 0.6)
    # plt.ylim(0, 0.1)
    # plt.show()

    else:
        print("No device found")
        sys.exit(1)

    for i in range(len(powers)):
        powers[i] = - powers[i]

    plt.plot(voltages, powers, '.')
    plt.xlim(0, 0.6)
    plt.ylim(0, 0.06)
    plt.show()