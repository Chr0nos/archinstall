from subprocess import run
import os


def install_grub_i386(device):
    run(['grub-install', '--target', 'i386-pc', device])


def install_grub_uefi(device):
    assert os.path.exists('/sys/firmware/efi')
    run(['grub-install', '--target', 'x86_64-efi', device])
