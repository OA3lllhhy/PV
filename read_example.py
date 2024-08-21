#!/usr/bin/env python
#
# Simple script showing how to stream data from a device in noncontinuous mode,
# use Ctrl-C to exit.

from __future__ import print_function

from signal import signal, SIG_DFL, SIGINT
import sys

from pysmu import Session, Mode


# If stdout is a terminal continuously overwrite a single line, otherwise
# output each line individually.
if sys.stdout.isatty():
    output = lambda s: sys.stdout.write("\r" + s)
else:
    output = print


if __name__ == '__main__':
    # don't throw KeyboardInterrupt on Ctrl-C
    signal(SIGINT, SIG_DFL)

    session = Session()

    if session.devices:
        # Grab the first device from the session.
        dev = session.devices[0]

        # Set both channels to high impedance mode.
        chan_a = dev.channels['A']
        chan_b = dev.channels['B']
        chan_a.mode = Mode.HI_Z
        chan_b.mode = Mode.HI_Z

        while True:
            # Run the session for 1000 samples in noncontinuous mode and read
            # incoming samples from both channels of the first device in a
            # blocking fashion.
            samples = dev.get_samples(1000)
            for x in samples:
                output("{: 6f} {: 6f} {: 6f} {: 6f}".format(x[0][0], x[0][1], x[1][0], x[1][1]))
    else:
        print('no devices attached')
