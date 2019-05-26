import os
import asyncio
import netdev
import git
from git.repo import Repo
from labber.device import Device


class Lab:
    def __init__(self, name, description, devices, basedir):
        self.name = name
        self.description = description
        self.path = os.path.expanduser(basedir)
        self.repo = self.init_repo()
        self.devices = self.init_devices(devices)

    def init_repo(self):
        os.makedirs(self.path, exist_ok=True)
        return Repo.init(self.path)

    def init_devices(self, devices):
        devs = []
        for t, hosts in devices.items():
            for h in hosts:
                d = Device(h, h, t, self.repo, "Cisco", "Cisco")
                devs.append(d)
        return devs

    async def run(self, func, devices):
        tasks = [getattr(dev, func)() for dev in devices]
        await asyncio.gather(*tasks)

    def get_config(self, devices):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run("get", devices))

    def commit_config(self, message, devices):
        self.repo.git.add([d.filename for d in devices])
        self.repo.index.commit(message)
