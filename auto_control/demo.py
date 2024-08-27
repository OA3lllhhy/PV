import sys
from pysmu import Session, Mode
from signal import signal, SIG_DFL, SIGINT


chan_a.constant(1)
chan_a.triangle(1, 0, 10, 0)
chan_a.sawtooth(1, 0, 10, 0)
chan_a.sine(1, 0, 10, 0)
chan_a.square(1, 0, 10, 0)
chan_a.stairstep(1, 0, 10, 0)