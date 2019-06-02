import netdev

from labber.device import Device


class IOSDevice(Device):

    device_type = "cisco_ios"
    _scp_path = "flash:/labber_replace_config.cfg"

    async def get_config(self):
        async with netdev.create(**dict(self)) as node:
            config = await node.send_command("show run")
            return [self, "\n".join(config.splitlines()[3:])]

    async def replace_config(self):
        # config replace is unreliable s
        async with netdev.create(**dict(self)) as node:
            await node.send_command(
                "copy flash:labber_replace_config.cfg startup-config",
                pattern=r"\[startup\-config\]\?",
            )
            await node.send_command("\n")
            await node.send_command(
                "reload reason labber:replace_config", pattern=r"\[confirm\]"
            )
            await node.send_command("\n")
            return
