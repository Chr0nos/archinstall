from subprocess import run
import os


def install_grub_i386(device):
    run(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'])
    run(['grub-install', '--target', 'i386-pc', device])


def install_grub_uefi(device):
    assert os.path.exists('/sys/firmware/efi')
    run(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'])
    run(['grub-install', '--target', 'x86_64-efi', device])


def install_trizen(user):
    user.run(
        ['git', 'clone', 'https://aur.archlinux.org/packages/trizen-git/'],
        cwd=user.home
    )
    user.run(['makepkg', '-si'], cwd=user.home + '/trizen-git')
    user.run(['rm', '-rf', user.home + '/trizen-git'])
