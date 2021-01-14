import os
from subprocess import run as subprocess_run
from contextlib import contextmanager


def run(*args, **kwargs):
    kwargs.setdefault('check', True)
    print(f'Command: ({args}) ({kwargs})')
    return subprocess_run(*args, **kwargs)


@contextmanager
def chroot(path, change_to='/'):
    real_root = os.open('/', os.O_RDONLY)
    cwd = os.getcwd()
    os.chroot(path)
    os.chdir(change_to)
    yield
    os.chdir(real_root)
    os.chroot('.')
    os.chdir(cwd)


@contextmanager
def cd(path):
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)


@contextmanager
def arch_chroot(path: str):
    assert path != '/'
    assert os.path.isdir(path)
    mount(f'{path}/proc', ['nosuid', 'noexec', 'nodev'], 'proc')
    mount(f'{path}/dev', ['mode=0755', 'nosuid'], 'devtmpfs')
    mount(f'{path}/dev/pts', ['nodev', 'nosuid'], 'devpts')
    mount(f'{path}/dev/shm', ['nodev', 'nosuid'], 'tmpfs')
    mount(f'{path}/run', ['nosuid,nodev,mode=755'], 'tmpfs')
    mount(f'{path}/tmp', ['mode=1777', 'strictatime', 'nodev', 'nosuid'],
          'tmpfs')
    mount(f'{path}/sys', ['nosuid', 'noexec', 'nodev', 'ro'], 'sysfs')
    with chroot(path):
        yield
    arch_chroot_unmount(path)


def arch_chroot_unmount(path: str):
    unmount(f'{path}/sys')
    unmount(f'{path}/tmp')
    unmount(f'{path}/run')
    unmount(f'{path}/dev/shm')
    unmount(f'{path}/dev/pts')
    unmount(f'{path}/dev')
    unmount(f'{path}/proc')


def mount(path: str, opts=None, fs_type=None, device=None):
    if os.path.ismount(path):
        return
    os.makedirs(path, exist_ok=True)
    args = []
    if opts:
        args.append('-o')
        args.append(','.join(opts))
    if fs_type:
        args.extend(['-t', fs_type])
    if not device and fs_type:
        device = fs_type
    if device:
        args.append(device)
    args.append(path)
    run(['mount'] + args)


def unmount(path: str, check=False):
    run(['umount', path], check=check)


def genfstab(root: str):
    run(['genfstab'], root)
