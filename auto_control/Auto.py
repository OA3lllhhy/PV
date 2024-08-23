from __future__ import print_function

from signal import signal, SIG_DFL, SIGINT
import random
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

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
        # plt.plot(x, voltage_data)
        # plt.plot(x, current_data)
        plt.plot(voltage_data, - current_data, '.')
        plt.plot(voltage_data, - current_data * voltage_data, '.')
        plt.xlim(0, 0.6)
        plt.ylim(0, 0.03)
        plt.grid()
        plt.show()


        session.end()
        
        
            
    else:
        print('no devices attached')