from subprocess import run


class UserNotFound(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class User:
    def __init__(self, username, gid=None):
        self.username = username
        self.gid = gid

    @staticmethod
    def load(username: str):
        with open('/etc/group') as grp_file:
            for line in grp_file.readlines():
                line = line[0:2]
                name, _, gid = line.split(':')
                if name == username:
                    return User(username, gid)
        raise UserNotFound(username)

    @staticmethod
    def create(username: str):
        try:
            User.load(username)
            raise UserAlreadyExists
        except UserNotFound:
            run(['useradd', '-m', username])
            return User.load(username)

    #TODO DEMOTE !!!
