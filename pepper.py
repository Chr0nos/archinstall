from archinstall.pacman import pacstrap, Pacman
from archinstall.utils import arch_chroot, run, arch_chroot_unmount, genfstab
from archinstall.users import User
from archinstall.services import Service, ServiceManager
from archinstall.helpers import install_grub_i386, install_trizen
import os


def setup_pepper(path='/mnt', boot_dev='/dev/vda'):
    arch_chroot_unmount(path)
    services = ServiceManager()
    services.add(Service('ssh', ['openssh'], 'sshd'))
    services.add(Service('docker', ['docker', 'docker-compose'], 'docker'))
    services.add(Service('network', ['network-manager'], 'NetworkManager'))
    services.add_many(Service.short_list(['gpm', 'acpid', 'iptables']))

    # bootstrap the system
    pacstrap(path, ['base', 'base-devel'])
    run(['vim', f'{path}/etc/pacman.conf'])
    run(['vim', f'{path}/etc/locale.gen'])
    open(f'{path}/etc/hostname', 'w').write('pepper\n')
    os.makedirs(f'{path}/etc/', exist_ok=True)
    run(['cp', '-v', '/etc/resolv.conf', f'{path}/etc/resolv.conf'])
    Pacman.sync()
    with arch_chroot(path):
        Pacman.install([
            'net-tools', 'wireguard-tools',
            'iptables', 'grub', 'vim', 'zsh', 'git', 'gcc', 'clang',
            'linux', 'linux-headers', 'linux-firmware', 'mkinitcpio', 'mdadm',
            'archlinux-keyring', 'sudo', 'wget', 'xfsprogs', 'tmux',
            *services.packages()
        ])
        run(['mkinitcpio', '-p', 'linux'])
        services.enable()
        os.makedirs('/etc/polkit-1/rules.d/', exist_ok=True)
        run(['ln', '-s', '/usr/share/zoneinfo/Europe/Paris', '/etc/localtime'])

        # setup my user account
        user, _ = User.get_or_create('adamaru')
        user.add_to_groups([
            'audio', 'video', 'wheel', 'docker', 'kvm', 'input', 'render'
        ])
        install_trizen(user)
        run(['passwd', user.username])
        run(['passwd'])

        install_grub_i386(boot_dev)
    genfstab(path)


if __name__ == "__main__":
    setup_pepper()
