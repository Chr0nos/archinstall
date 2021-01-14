from subprocess import run
from archinstall.pacman import Pacman
import os


def install_grub_i386(device):
    run(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'])
    run(['grub-install', '--target', 'i386-pc', device])


def install_grub_uefi(device):
    assert os.path.exists('/sys/firmware/efi')
    run(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'])
    run(['grub-install', '--target', 'x86_64-efi', device])


def install_trizen(user):
    trizen_path = user.home + '/trizen-git'
    Pacman.install([
        'pacutils',
        'perl-libwww',
        'perl-term-ui',
        'perl-json',
        'perl-data-dump',
        'perl-lwp-protocol-https',
        'erl-term-readline-gnu'
    ])
    if not os.path.exists(trizen_path):
        user.run(
            ['git', 'clone', 'https://aur.archlinux.org/trizen-git/'],
            cwd=user.home
        )
    user.run(['makepkg', '-si'], cwd=trizen_path)
    user.run(['rm', '-rf', trizen_path])
