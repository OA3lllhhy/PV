"""
Demo of getting the reading of channel A
"""
from pysmu import Session, Mode
import time

session = Session()

if len(session.devices) == 0:
    print("No devices found")
    exit()

devx = session.devices[0]

# Set the channel A to source voltage with triangle input and measure current
CHA = devx.channels['A']
CHA.mode = Mode.SVMI
CHA.triangle(1, 0, 1, 0)

# Set the channel B to high impedance
CHB = devx.channels['B']
CHB.mode = Mode.HI_Z

# Start the session
session.start(0)

# Get the reading of channel A
samples = devx.get_samples(1)
print(samples)


# Close the session
session.end()
