from pysmu import Session
session = Session()
devx = session.devices[0]
devx.serial
print(devx.serial)

print(devx.fwver)

print(devx.hwver)