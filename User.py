from abc import ABC, abstractmethod

from Post import FactoryPost


class Sender(ABC):

    def __init__(self):
        self.followers = set()

    @abstractmethod
    def follow(self, member):
        pass

    @abstractmethod
    def unfollow(self, member):
        pass

    def notify(self, notification):
        for followers in self.followers:
            followers.update(notification)


class Member(ABC):

    @abstractmethod
    def update(self, liker):
        pass


class UserName(Sender, Member, ABC):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.is_logged_in = False
        self.notifications = []
        self.posts = []

    def follow(self, user):
        if not self.is_logged_in:
            raise ValueError("You are not authorized to follow because you are not logged in.")
        user.followers.add(self)
        print(self.username + " started following " + user.username)

    def unfollow(self, user):
        if not self.is_logged_in:
            raise ValueError("You are not authorized to unfollow because you are not logged in.")
        user.followers.remove(self)
        print(self.username + " unfollowed " + user.username)

    def publish_post(self, post_type, content, price=None, location=None):
        if not self.is_logged_in:
            raise ValueError("You are not authorized to publish post because you are not logged in.")
        post = FactoryPost.creat_post(self, post_type, content, price, location)
        self.posts.append(post)
        self.notify(notification=f"{self.username} has a new post")
        return post

    def update(self, notification):
        self.notifications.append(notification)

    def print_notifications(self):
        print(f"{self.username}'s notifications:")
        for notification in self.notifications:
            print(notification)

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"
