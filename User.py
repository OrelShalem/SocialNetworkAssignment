from abc import ABC, abstractmethod

from Post import FactoryPost


class Sender(ABC):
    """
    Abstract base class representing a sender of messages or updates.

    Attributes:
        followers (set[Member]): A set of members who follow this sender.
    """

    def __init__(self):
        self.followers = set()

    @abstractmethod
    def follow(self, member):
        """
        Abstract method to follow another member.

        Args:
            member (Member): The member to follow.
        """
        pass

    @abstractmethod
    def unfollow(self, member):
        """
        Abstract method to unfollow another member.

        Args:
            member (Member): The member to unfollow.
        """
        pass

    def notify(self, notification):
        """
        Sends a notification to all followers.

        Args:
            notification (str): The notification message.
        """
        for follower in self.followers:
            follower.update(notification)


class Member(ABC):
    """
    Abstract base class representing a member who can receive updates.

    @abstractmethod
    def update(self, liker):
        pass
    """
    pass


class UserName(Sender, Member, ABC):
    """
    Concrete class representing a user in the social network with functionalities
    of sending messages, receiving notifications, and managing followers.

    Attributes:
        username (str): The user's username.
        password (str): The user's password.
        is_logged_in (bool): Whether the user is logged in.
        notifications (list[str]): A list of received notifications.
        posts (list[Post]): A list of posts created by the user.
    """

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.is_logged_in = False
        self.notifications = []
        self.posts = []

    def follow(self, user):
        """
        Follows another user.

        Args:
            user (UserName): The user to follow.

        Raises:
            ValueError: If the user is not logged in.
        """

        if not self.is_logged_in:
            raise ValueError("You are not authorized to follow because you are not logged in.")
        user.followers.add(self)
        print(self.username + " started following " + user.username)

    def unfollow(self, user):
        """
        Unfollows another user.

        Args:
            user (UserName): The user to unfollow.

        Raises:
            ValueError: If the user is not logged in.
        """

        if not self.is_logged_in:
            raise ValueError("You are not authorized to unfollow because you are not logged in.")
        user.followers.remove(self)
        print(self.username + " unfollowed " + user.username)

    def publish_post(self, post_type, content, price=None, location=None):
        """
        Publishes a new post.

        Args:
            post_type (str): The type of post to create (e.g., "text", "image").
            content (str): The content of the post.
            price (float, optional): The price of the post (if applicable).
            location (str, optional): The location of the post (if applicable).

        Returns:
            Post: The newly created post object.

        Raises:
            ValueError: If the user is not logged in.
        """

        if not self.is_logged_in:
            raise ValueError("You are not authorized to publish post because you are not logged in.")
        post = FactoryPost.creat_post(self, post_type, content, price, location)
        self.posts.append(post)
        self.notify(notification=f"{self.username} has a new post")
        return post

    def update(self, notification):
        """
        Receives a notification.

        Args:
            notification (str): The notification message.
        """

        self.notifications.append(notification)

    def print_notifications(self):
        """
        Prints all received notifications.
        """

        print(f"{self.username}'s notifications:")
        for notification in self.notifications:
            print(notification)

    def __str__(self):
        """
        Returns a string
        """
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"
