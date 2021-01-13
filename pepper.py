from archinstall.pacman import Pacman, pacstrap, run
from archinstall.utils import arch_chroot
from archinstall.users import User
from archinstall.helpers import install_grub_i386
import os


def setup_pepper(path='/mnt', boot_dev='/dev/vda'):
    # bootstrap the system
    pacstrap(
        path, [
            'base',
            'base-devel',
        ]
    )
    run(['vim', '/etc/pacman.conf'])
    run(['vim', '/etc/locale.gen'])
    run('echo pepper > /etc/hostname', shell=True)
    run(['cp', '-v', '/etc/resolv.conf', f'{path}/etc/resolv.conf'])
    pacman = Pacman()
    pacman.add_many([
        'net-tools', 'networkmanager', 'wireguard-tools', 'fail2ban',
        'iptables', 'grub', 'vim', 'zsh', 'git', 'gcc', 'clang', 'docker',
        'linux', 'linux-headers', 'linux-firmware', 'mkinitramfs', 'mdadm',
        'archlinux-keyring', 'sudo', 'wget', 'xfsprogs'
    ])
    with arch_chroot(path):
        pacman.sync().install()
        run(['grub-mkconfig', '-o', '/boot/grub.cfg'])
        run(['mkinitcpio', '-p', 'linux'])
        for service in ('iptables', 'fail2ban', 'docker'):
            run(['systemctl', 'enable', service])
        os.makedirs('/etc/polkit-1/rules.d/', exist_ok=True)
        run(['ln', '-s', '/usr/share/zoneinfo/Europe/Paris', '/etc/localtime'])

        # setup my user account
        user = User.create('adamaru')
    install_grub_i386(boot_dev)
    with arch_chroot(path):
        run(['passwd'])


if __name__ == "__main__":
    setup_pepper()
