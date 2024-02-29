from enum import Enum
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class PostType(Enum):
    TEXT = 'Text'
    IMAGE = 'Image'
    SALE = 'Sale'


class Post(ABC):
    def __init__(self, user, content):
        self.user = user
        self.content = content
        self.likes = 0
        self.comments = 0
        self.likers = []

    def like(self, liker):
        if not liker.is_logged_in:
            raise ValueError("You are not authorized to like because you are not logged in.")
        # if self.user.username is liker.username:
        #     raise ValueError("You are not authorized to like on your post.")
        self.likes += 1
        self.likers.append(liker)
        if self.user.username is not liker.username:
            self.user.notifications.append(f"{liker.username} liked your post")
            print(f"notification to {self.user.username}: {liker.username} liked your post")

    def comment(self, user, comment):
        if not user.is_logged_in:
            raise ValueError("You are not authorized to comment because you are not logged in.")
        self.comments += 1
        if self.user.username is not user.username:
            self.user.notifications.append(f"{user.username} commented on your post")
            print(f"notification to {self.user.username}: {user.username} commented on your post: {comment}")

    @abstractmethod
    def __str__(self):
        self.__str__()


class FactoryPost:
    def creat_post(self, post_type, content, price=None, location=None):
        if post_type == PostType.TEXT.value:
            return TextPost(self, content)
        elif post_type == PostType.IMAGE.value:
            return ImagePost(self, content)
        elif post_type == PostType.SALE.value:
            return SalePost(self, content, price, location)


class TextPost(Post):
    def __init__(self, user, content):
        super().__init__(user, content)
        print(self.__str__())

    def __str__(self):
        return f"{self.user.username} published a post:\n\"{self.content}\"\n"


class ImagePost(Post):
    def __init__(self, user, content):
        super().__init__(user, content)
        print(self.__str__())

    def display(self):
        try:
            image = mpimg.imread(self.content)
        except FileNotFoundError:
            print(f"the picture not found int {self.content}")
            return
        plt.imshow(image)
        plt.show()
        print("Shows picture")

    def __str__(self):
        return f"{self.user.username} posted a picture\n"


class SalePost(Post):
    def __init__(self, user, product, price, location):
        super().__init__(user, product)
        self.price = price
        self.location = location
        self.is_product_available = True
        print(self.__str__())

    def discount(self, percent, password):
        if not self.user.is_logged_in:
            raise ValueError("You are not authorized to sold because you are not logged in.")
        if password is not self.user.password:
            raise ValueError("password invalid.")
        new_percent = (100 - percent) / 100
        new_price = self.price * new_percent
        self.price = new_price
        print(f"Discount on {self.user.username} product! the new price is: {self.price}")

    def sold(self, password):
        if not self.user.is_logged_in:
            raise ValueError("You are not authorized to sold because you are not logged in.")
        if password is not self.user.password:
            raise ValueError("password invalid.")
        self.is_product_available = False
        print(f"{self.user.username}'s product is sold")

    def __str__(self):
        if not self.is_product_available:
            return (f"{self.user.username} posted a product for sale:"
                    f"\nSold! {self.content},"
                    f" price: {self.price},"
                    f" pickup from: {self.location}\n")
        return (f"{self.user.username} posted a product for sale:"
                f"\nFor sale! {self.content},"
                f" price: {self.price},"
                f" pickup from: {self.location}\n")
