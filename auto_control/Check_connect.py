"""
This python script provide a quick way to check the ADALM is connected
"""
from pysmu import Session, Mode
session = Session()


if session.devices:
    print("ADALM-1000 is connected")
    print("Serial number: ", session.devices[0].serial)
    print("Firmware version: ", session.devices[0].fwver)
    print("Hardware version: ", session.devices[0].hwver)

else:
    print("ADALM-1000 is not connected")