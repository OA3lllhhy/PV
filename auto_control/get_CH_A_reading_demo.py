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
CHA.triangle(0.1, 0.1, 0.1, 0)
# CHA.current_limit(0.1)

# Run for 20 times and get the readings
for i in range(20):
    print(CHA.measure())
    time.sleep(0.1)

# Close the session
session.end()
