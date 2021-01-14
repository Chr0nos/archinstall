from archinstall.utils import run


class Pacman:
    @staticmethod
    def sync():
        return run(['/usr/bin/pacman', '-Sy'])

    @staticmethod
    def install(packages):
        return run(['/usr/bin/pacman', '-S', '--noconfirm'] + packages)


def pacstrap(path: str, packages):
    run(['pacstrap', path] + packages)
