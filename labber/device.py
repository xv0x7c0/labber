import asyncio
import io
import netdev
import os


class Device:
    def __init__(self, hostname, filename, device_type, repository, username, password):
        self.hostname = hostname
        self.filename = filename
        self.device_type = device_type
        self.repository = repository
        self.username = username
        self.password = password

    def netdev(self):
        return {
            "host": self.hostname,
            "device_type": self.device_type,
            "username": self.username,
            "password": self.password,
        }

    def checkout(self, commit_id="HEAD"):
        c = self.repository.commit(commit_id)
        f = c.tree / self.filename
        with io.BytesIO(f.data_stream.read()) as file:
            return file.read().decode("utf-8")

    def write(self, config):
        dst = os.path.join(self.repository.working_tree_dir, self.filename)
        with open(dst, "w") as file:
            file.write(config)

    async def get(self):
        async with netdev.create(**self.netdev()) as node:
            config = await node.send_command("show run")
            self.write("\n".join(config.splitlines()[3:]))
