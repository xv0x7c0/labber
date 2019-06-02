from labber.cisco.ios_device import IOSDevice
from labber.cisco.xr_device import XRDevice

class DeviceBuilder:

    def build(hostname, filename, username, password, device_type):
        if device_type == "cisco_ios":
          return IOSDevice(hostname, filename, username, password)
        elif device_type == "cisco_ios_xr":
          return XRDevice(hostname, filename, username, password)
        else:
          raise NotImplementedError("Device type '{}' is unknown".format(device_type))
