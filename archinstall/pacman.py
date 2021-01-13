from subprocess import run


class Pacman:
    def __init__(self):
        self.packages = []
        self.bin = '/usr/bin/pacman'

    def __str__(self):
        return ' '.join(self.packages)

    def add(self, package):
        self.packages.append(package)
        return self

    def add_many(self, packages):
        self.packages.extend(packages)
        return self

    def sync(self):
        run([self.bin, '-Sy'])
        return self

    def install(self):
        run([self.bin, '-S', '--noconfirm'] + self.packages)

    def remove(self, package):
        try:
            self.packages.remove(package)
        except ValueError:
            pass
        run([self.bin, '-Rns', package])


def pacstrap(path: str, packages):
    run(['pacstrap'] + packages)
