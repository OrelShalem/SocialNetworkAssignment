from User import UserName


class SocialNetwork(object):
    """
    Represents a social network with user management functionalities.

    Attributes: name (str): The name of the social network. list_of_username (list[str]): [Optional] List of
    usernames for potential redundancy check. Not currently used in this implementation. usernames (dict[str,
    UserName]): Dictionary to store usernames and their corresponding User objects.
    """

    _instance = None  # Private attribute to implement singleton pattern

    def __new__(cls, name):
        """
        Creates a new SocialNetwork instance or returns the existing one.

        Args:
            name (str): The name of the social network to be created.

        Returns:
            SocialNetwork: An instance of the SocialNetwork class.

        Raises:
            TypeError: If the name is not a string.
        """

        if not isinstance(name, str):
            raise TypeError("Social network name must be a string.")

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.name = name
            cls._instance.list_of_username = []  # Optional attribute, not used currently
            cls._instance.usernames = {}
            print("The social network " + name + " was created!")
        return cls._instance

    def sign_up(self, username, password):
        """
        Creates a new user account in the social network.

        Args:
            username (str): The desired username for the new user.
            password (str): The password for the new user.

        Returns:
            UserName: The newly created UserName object.

        Raises:
            ValueError: If the username already exists or the password is invalid.
        """

        if username in self.usernames:
            raise ValueError("The username " + username + " already exists!")
        if not 4 <= len(password) <= 8:
            raise ValueError("The password " + password + " is invalid. It must be between 4 and 8 characters long.")

        new_user = UserName(username, password)
        new_user.is_logged_in = True
        self.usernames[username] = new_user
        return new_user

    def log_out(self, username):
        """
        Logs out a user from the social network.

        Args:
            username (str): The username of the user to log out.

        Returns:
            None
        """

        if username in self.usernames:
            self.usernames[username].is_logged_in = False
            print(username + " disconnected")
        else:
            print(username + " is not a registered user.")

    def log_in(self, username, password):
        """
        Logs a user into the social network.

        Args:
            username (str): The username of the user to log in.
            password (str): The password of the user.

        Returns:
            None
        """

        if username not in self.usernames:
            print(username + " is not a registered user.")
            return

        if password != self.usernames[username].password:
            print("Invalid password for user " + username + ".")
            return

        self.usernames[username].is_logged_in = True
        print(username + " connected")

    def __str__(self):
        """
        Returns a string representation of the social network, including its name and all registered users.

        Returns:
            str: A string representation of the social network details.
        """

        users = f"{self.name} social network:\n"
        for username in self.usernames.values():
            users += str(username) + "\n"
        return users
