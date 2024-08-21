import pysmu
from pysmu import Session

# Create a session
session = Session()

# Add devices to the session
if not session.devices:
    print("No devices found. Please connect your ADALM1000.")
    exit(1)

device = session.devices[0]  # Use the first connected device

# Configure Channel A for Source Voltage and Measure Current (SVMI)
channel_a = device.channels['A']
channel_a.mode = pysmu.Mode.SVMI
channel_a.constant(1.0)  # Set a constant voltage of 1.0 Volt

# Start sampling
session.start(10)  # Start data acquisition

try:
    # Continuously read and print data
    for i in range(100):  # Limiting to 100 readings for example purposes
        #session.update(10)  # Read 10 samples from the device
        voltage = channel_a.measured_voltage
        current = channel_a.measured_current
        print(f"Voltage: {voltage:.3f} V, Current: {current:.6f} A")
finally:
    session.end()  # Stop the session and clean up

