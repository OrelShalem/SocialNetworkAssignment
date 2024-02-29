from User import UserName


# class Singleton(type):
#     _instance = None
#
#     def __new__(cls, name):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls, name)
#             cls.list_of_username = []
#             cls.usernames = {}
#             cls.name = name
#             print("The social network " + name + " was created!")
#         return cls._instance


class SocialNetwork(object):
    _instance = None

    def __new__(cls, name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.name = name
            cls._instance.list_of_username = []
            cls._instance.usernames = {}
            print("The social network " + name + " was created!")
        return cls._instance

    def sign_up(self, username, password):
        if username in self.usernames:
            raise ValueError("The username " + username + " already exists!")
        if not 4 <= len(password) <= 8:
            raise ValueError("The password " + password + " invalid")
        new_user = UserName(username, password)
        new_user.is_logged_in = True
        self.usernames[username] = new_user
        return new_user

    def log_out(self, username):
        if username in self.usernames:
            self.usernames[username].is_logged_in = False
            print(username + " disconnected")
        else:
            return

    def log_in(self, username, password):
        if username not in self.usernames:
            return
        if password != self.usernames[username].password:
            return
        self.usernames[username].is_logged_in = True
        print(username + " connected")

    def __str__(self):
        users = f"{self.name} social network:\n"
        for username in self.usernames.values():
            users += str(username) + "\n"
        return users
