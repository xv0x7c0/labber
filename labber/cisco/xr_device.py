import netdev

from labber.device import Device


class XRDevice(Device):

    device_type = "cisco_ios_xr"
    _scp_path = "disk0:/labber_replace_config.cfg"

    async def get_config(self):
        async with netdev.create(**dict(self)) as node:
            config = await node.send_command("show run")
            return [self, "\n".join(config.splitlines()[3:])]

    async def replace_config(self):
        async with netdev.create(**dict(self)) as node:
            await node.send_command("configure exclusive")
            await node.send_command("load disk0:labber_replace_config.cfg")
            await node.send_command("commit replace", pattern=r"\[no\]\:")
            await node.send_command("yes")
