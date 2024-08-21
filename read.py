import sys
from pysmu import *

session = Session()
session.add_all()

if len(session.devices) == 0:
    sys.stderr.write("Plub in a device.\n")
    sys.exit(1)

device = next(iter(session.devices))
rxbuf = []

while True:
    session.run(1024)

    try: 
        device.read(rxbuf, 1024)
    # except Exception as e:
    #     sys.stderr.write(f"sample(s) dropped: {e}\n")
    #     sys.exit(1)

    for i in rxbuf:
        if sys.stdout.isatty():
            print(f"\r{i[0]:6f} {i[1]:6f} {i[2]:6f} {i[3]:6f}", end='')
        else:
            print(f"{i[0]:6f} {i[1]:6f} {i[2]:6f} {i[3]:6f}")
