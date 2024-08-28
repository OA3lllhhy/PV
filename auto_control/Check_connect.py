"""
This python script provide a quick way to check the ADALM is connected
"""
from pysmu import Session
session = Session()
devx = session.devices[0]
devx.serial
print(devx.serial)
print(devx.fwver)
print(devx.hwver)