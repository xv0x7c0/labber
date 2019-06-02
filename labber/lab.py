import asyncio
import io
import os

import netdev
from git.repo import Repo

from labber.device_builder import DeviceBuilder


class Lab:
    def __init__(self, name, description, devices, basedir):
        self.name = name
        self.description = description
        self.path = os.path.expanduser(basedir)
        self.repository = self.init_repository()
        self.devices = self.init_devices(devices)

    def init_repository(self):
        os.makedirs(self.path, exist_ok=True)
        return Repo.init(self.path)

    def init_devices(self, devices):
        devs = []
        for t, hosts in devices.items():
            for h in hosts:
                d = DeviceBuilder.build(h, h, "Cisco", "Cisco", t)
                devs.append(d)
        return devs

    async def run(self, func, devices, *args):
        tasks = [getattr(dev, func)(*args) for dev in devices]
        return await asyncio.gather(*tasks)

    def get_configs(self, devices):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run("get_config", devices))

    def replace_configs(self, devices):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run("replace_config", devices))

    def send_configs(self, devices, configs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run("send_config", devices, configs))

    def write_configs(self, configs):
        for device, config in configs:
            dst = os.path.join(self.repository.working_tree_dir, device.filename)
            with open(dst, "w") as f:
                f.write(config)

    def commit_configs(self, message, devices):
        filenames = [device.filename for device in devices]
        self.repository.git.add(filenames)
        self.repository.index.commit(message)

    def get_configs_revision(self, commit_id, devices):
        configs = []
        commit_id = commit_id or "HEAD"
        commit = self.repository.commit(commit_id)
        devices_filenames = [device.filename for device in devices]
        tree_filenames = [blob.name for blob in commit.tree.blobs]

        if devices_filenames == tree_filenames:
            for device in devices:
                blob = commit.tree / device.filename
                with io.BytesIO(blob.data_stream.read()) as f:
                    configs.append([device, f.read().decode("utf-8")])
        else:
            raise Exception("Some filenames did not exist at this point")

        return configs
