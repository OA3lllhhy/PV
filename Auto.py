from __future__ import print_function

from signal import signal, SIG_DFL, SIGINT
import random
import sys
import time

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
        chan_a.triangle(1, 0, 10, 0)
        chan_b.triangle(1, 0, 10, 0)

        # start a continous session with 1000 samples store all the data in a dataframe
        start_time = time.time()
        session.start(100)
        all_data = []
        i = 0

        while True:
            if time.time() - start_time >= 1:
                break
            else:
                samples = dev.get_samples(100)
                print(samples)
                for x in samples:
                    all_data.append(samples)
                    i = i+1
                    # output("{: 6f} {: 6f} {: 6f} {: 6f}".format(x[0][0], x[0][1], x[1][0], x[1][1]))
        print(i)
        session.end()
            
    else:
        print('no devices attached')