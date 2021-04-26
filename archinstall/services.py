from typing import List
from archinstall.utils import run


class Service:
    name = None
    packages = []
    services = []

    def __init__(self, name: str, packages = List[str], services = List[str]):
        self.name = name
        self.packages = packages
        self.services = services if not isinstance(services, str) \
            else [services]

    @classmethod
    def short(cls, name: str):
        return cls(name, [name], [name])

    @classmethod
    def short_list(cls, names):
        return [cls(name, [name], [name]) for name in names]

    def __str__(self):
        return self.name

    def enable(self):
        for service in self.services:
            run(['systemctl', 'enable', service])
        return self


class ServiceManager:
    def __init__(self):
        self.members = []

    def __str__(self):
        return ', '.join([member.name for member in self.members])

    def add(self, service: Service):
        self.members.append(service)
        return self

    def add_many(self, services):
        self.members.extend(services)
        return self

    def packages(self) -> List[str]:
        pkgs = []
        for service in self.members:
            pkgs.extend(service.packages)
        return pkgs

    def enable(self):
        for service in self.members:
            service.enable()
        return self
