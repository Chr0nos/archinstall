import os
from archinstall.utils import run


class UserNotFound(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class User:
    def __init__(self, username, uid=None, gid=None, home=None):
        self.username = username
        self.gid = gid
        self.uid = uid
        self.home = home if home else f'/home/{username}'
        self.groups = self.get_groups()

    def __str__(self):
        return f'{self.username} (uid: {self.uid} gid: {self.gid}) ' \
               f'[{", ".join(self.groups.keys())}]'

    @property
    def env(self):
        path = os.environ.get('PATH', '')
        return {
            'HOME': self.home,
            'PWD': self.home,
            'USER': self.username,
            'LOGNAME': self.username,
            'EDITOR': 'vim',
            'OLDPWD': '/',
            'TERM': 'linux',
            'PATH': f'{self.home}/.local/bin/:{path}'
        }

    @staticmethod
    def load(username: str):
        with open('/etc/passwd') as passwd_file:
            for line in passwd_file.readlines():
                name, _, uid, gid, desc, home, shell = line.split(':')
                gid = int(gid)
                uid = int(uid)
                if name == username:
                    return User(name, uid, gid, home)
        raise UserNotFound(username)

    def get_groups(self):
        def get_subscribed_groups(line):
            group, _, gid, usernames = line.split(':')
            usernames = usernames.split(',')
            if self.username in usernames:
                return group, gid

        groups = {}
        with open('/etc/group') as grp_file:
            for line in grp_file.readlines():
                group, _, gid, usernames = line.split(':')
                usernames = usernames.split(',')
                if self.username in usernames:
                    groups[group] = int(gid)
        return groups

    @staticmethod
    def create(username: str):
        try:
            User.load(username)
            raise UserAlreadyExists
        except UserNotFound:
            run(['useradd', '-m', username])
            return User.load(username)

    @staticmethod
    def get_or_create(username):
        try:
            return User.load(username), False
        except UserNotFound:
            return User.create(username), True

    def demote(self):
        assert self.uid is not None
        assert self.gid is not None
        # print(f'Demote to {self.username} ({self.uid}:{self.gid}) '
        #       f'[{", ".join(self.groups.keys())}]')
        os.setgroups(tuple(self.groups.values()))
        os.setgid(self.gid)
        os.setuid(self.uid)

    def run(self, *args, **kwargs):
        kwargs.setdefault('preexec_fn', self.demote)
        kwargs.setdefault('env', self.env)
        return run(*args, **kwargs)

    def add_to_group(self, group: str):
        run(['gpasswd', '-a', self.username, group])

    def add_to_groups(self, groups):
        for group in groups:
            run(['gpasswd', '-a', self.username, group])
