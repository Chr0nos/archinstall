from subprocess import run


class Pacman:
    @staticmethod
    def sync():
        return run(['/usr/bin/pacman', '-Sy'])

    @staticmethod
    def install(packages):
        return run(['/usr/bin/pacman', '-S', '--no-confirm'] + packages)


def pacstrap(path: str, packages):
    run(['pacstrap'] + packages)
