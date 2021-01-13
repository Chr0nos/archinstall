import os
from subprocess import run
from contextlib import contextmanager


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
    real_root.close()


@contextmanager
def cd(path):
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)


@contextmanager
def arch_chroot(path):
    mount(f'{path}/proc', ['nosuid', 'noexec', 'nodev'], 'proc')
    mount(f'{path}/dev', ['mode=0755', 'nosuid'], 'devtmpfs')
    mount(f'{path}/dev/pts', ['nodev', 'nosuid'], 'devpts')
    mount(f'{path}/dev/shm', ['nodev', 'nosuid'], 'tmpfs')
    mount(f'{path}/run', ['nosuid,nodev,mode=755'], 'tmpfs')
    mount(f'{path}/tmp', ['mode=1777', 'sctrictaname', 'nodev', 'nosuid'],
          'tmpfs')
    mount(f'{path}/sys', ['nosuid', 'noexec', 'nodev', 'ro'], 'sysfs')
    with chroot(path):
        yield
    unmount(f'{path}/sys')
    unmount(f'{path}/tmp')
    unmount(f'{path}/run')
    unmount(f'{path}/dev/shm')
    unmount(f'{path}/dev/pts')
    unmount(f'{path}/dev')
    unmount(f'{path}/dev/proc')


def mount(path: str, opts=None, fs_type=None, device=None):
    args = [path]
    if opts:
        args.extend(','.join(opts))
    if fs_type:
        args.extend(['-t', fs_type])
    if not device and fs_type:
        device = fs_type
    if device:
        args.append(device)
    run(['mount'] + args)


def unmount(path: str, check=False):
    run(['umount', path], check=check)
