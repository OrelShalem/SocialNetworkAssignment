from enum import Enum
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class PostType(Enum):
    """
    Enumeration representing different types of posts.
    """
    TEXT = 'Text'
    IMAGE = 'Image'
    SALE = 'Sale'


class Post(ABC):
    """
    Abstract base class representing a post in the social network.

    Attributes:
        user (UserName): The user who created the post.
        content (str): The content of the post.
        likes (int): The number of likes the post has received.
        comments (int): The number of comments the post has received.
        likers (list[UserName]): A list of users who liked the post.
    """

    def __init__(self, user, content):
        self.user = user
        self.content = content
        self.likes = 0
        self.comments = 0
        self.likers = []

    def like(self, liker):
        """
        Likes a post.

        Args:
            liker (UserName): The user who is liking the post.

        Raises:
            ValueError: If the user is not logged in.
            # Removed check for liking own post as it can be enabled/disabled based on requirements.
        """

        if not liker.is_logged_in:
            raise ValueError("You are not authorized to like because you are not logged in.")

        self.likes += 1
        self.likers.append(liker)
        if self.user.username is not liker.username:
            self.user.notifications.append(f"{liker.username} liked your post")
            print(f"notification to {self.user.username}: {liker.username} liked your post")

    def comment(self, user, comment):
        """
        Comments on a post.

        Args:
            user (UserName): The user who is commenting on the post.
            comment (str): The content of the comment.

        Raises:
            ValueError: If the user is not logged in.
        """

        if not user.is_logged_in:
            raise ValueError("You are not authorized to comment because you are not logged in.")

        self.comments += 1
        if self.user.username is not user.username:
            self.user.notifications.append(f"{user.username} commented on your post")
            print(f"notification to {self.user.username}: {user.username} commented on your post: {comment}")

    @abstractmethod
    def __str__(self):
        """
        Abstract method to return a string representation of the post.
        """
        pass


class FactoryPost:
    """
    Factory class to create different types of posts based on the specified type.
    """

    def creat_post(self, post_type, content, price=None, location=None):
        """
        Creates a post based on the specified type and arguments.

        Args:
            post_type (PostType): The type of post to create.
            content (str): The content of the post.
            price (float, optional): The price of the post (for sale posts only).
            location (str, optional): The location of the post (for sale posts only).

        Returns:
            Post: The created post object.
        """

        if post_type == PostType.TEXT.value:
            return TextPost(self, content)
        elif post_type == PostType.IMAGE.value:
            return ImagePost(self, content)
        elif post_type == PostType.SALE.value:
            return SalePost(self, content, price, location)


class TextPost(Post):
    """
    Concrete class representing a text post.
    """

    def __init__(self, user, content):
        super().__init__(user, content)
        print(self.__str__())

    def __str__(self):
        """
        Returns a string representation of the text post.
        """
        return f"{self.user.username} published a post:\n\"{self.content}\"\n"


class ImagePost(Post):
    """
    Concrete class representing an image post.
    """

    def __init__(self, user, content):
        super().__init__(user, content)
        print(self.__str__())

    def display(self):
        """
        Displays the image post.

                Raises:
                    FileNotFoundError: If the image file is not found.
                """

        try:
            image = mpimg.imread(self.content)
        except FileNotFoundError:
            raise ValueError(f"the picture not found in {self.content}")
        plt.imshow(image)
        plt.show()
        print("Shows picture")

    def __str__(self):
        """
        Returns a string representation of the image post.
        """
        return f"{self.user.username} posted a picture\n"


class SalePost(Post):
    """
        Concrete class representing a sale post.

        Attributes:
            price (float): The price of the product being sold.
            location (str): The location where the product can be picked up.
            is_product_available (bool): Whether the product is still available for sale.
        """

    def __init__(self, user, product, price, location):
        super().__init__(user, product)
        self.price = price
        self.location = location
        self.is_product_available = True
        print(self.__str__())

    def discount(self, percent, password):
        """
            Applies a discount to the product price.

            Args:
                percent (float): The discount percentage.
                password (str): The user's password to authorize the discount.

            Raises:
                ValueError: If the user is not logged in or the password is incorrect.
            """

        if not self.user.is_logged_in:
            raise ValueError("You are not authorized to sold because you are not logged in.")
        if password is not self.user.password:
            raise ValueError("password invalid.")
        new_percent = (100 - percent) / 100
        new_price = self.price * new_percent
        self.price = new_price
        print(f"Discount on {self.user.username} product! the new price is: {self.price}")

    def sold(self, password):
        """
            Marks the product as sold.

            Args:
                password (str): The user's password to authorize the sale.

            Raises:
                ValueError: If the user is not logged in or the password is incorrect.
            """

        if not self.user.is_logged_in:
            raise ValueError("You are not authorized to sold because you are not logged in.")
        if password is not self.user.password:
            raise ValueError("password invalid.")
        self.is_product_available = False
        print(f"{self.user.username}'s product is sold")

    def __str__(self):
        """
            Returns a string representation of the sale post.

            """

        if not self.is_product_available:
            return (f"{self.user.username} posted a product for sale:"
                    f"\nSold! {self.content},"
                    f" price: {self.price},"
                    f" pickup from: {self.location}\n")
        return (f"{self.user.username} posted a product for sale:"
                f"\nFor sale! {self.content},"
                f" price: {self.price},"
                f" pickup from: {self.location}\n")
