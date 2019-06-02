import os
import tempfile

import asyncssh
import netdev


class Device:
    def __init__(self, hostname, filename, username, password):
        self.hostname = hostname
        self.filename = filename
        self.username = username
        self.password = password

    def __iter__(self):
        yield "host", self.hostname
        yield "device_type", self.device_type
        yield "username", self.username
        yield "password", self.password

    async def send_config(self, configs):
        config = next(config[1] for config in configs if config[0] is self)
        config = config[:-1]
        tmpfile = tempfile.NamedTemporaryFile("w", delete=False)
        tmpfile.write(config)
        tmpfile.close()
        async with asyncssh.connect(
            self.hostname,
            username=self.username,
            password=self.password,
            known_hosts=None,
        ) as conn:
            await asyncssh.scp(tmpfile.name, (conn, self._scp_path))
        os.unlink(tmpfile.name)
