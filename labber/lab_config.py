import os
import yaml

from labber.device_builder import DeviceBuilder
from labber.lab import Lab
from git.repo import Repo


class LabConfig:
    def load(filepath):
        yaml = LabConfig.get_yaml(os.path.expanduser(filepath))
        devices = LabConfig.get_devices(yaml)
        name = yaml["name"]
        description = yaml["description"]
        repository = LabConfig.get_repo(yaml["basedir"])
        return Lab(name, description, devices, repository)

    def get_yaml(filepath):
        try:
            with open(filepath, "r") as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
        except yaml.YAMLError as err:
            print(err)

    def get_repo(filepath):
        fpath = os.path.expanduser(filepath)
        os.makedirs(fpath, exist_ok=True)
        return Repo.init(fpath)

    def get_devices(yaml):
        devs = []
        username = yaml["credentials"]["username"]
        password = yaml["credentials"]["password"]

        for device_type, hosts in yaml["devices"].items():
            for host_attribute in hosts:
                d = DeviceBuilder.build(
                    host_attribute["hostname"],
                    host_attribute["filename"],
                    username,
                    password,
                    device_type,
                )
                devs.append(d)

        return devs
