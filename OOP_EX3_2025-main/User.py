import copy

import Book
from abc import abstractmethod, ABC
from Search import Strategy
import Inventory


class Observer(ABC):
    """
    Interface for Observers in the Observer design pattern.
    """

    @abstractmethod
    def update(self, massage: str):
        """
        Update the observer with a change in the subject.

        :param massage: The message to update the observer with.
        """
        pass

class User(Observer):
    """
    A class representing a user, which is an observer in the observer pattern.
    """

    def __init__(self, username, password):
        """
        Initialize a new User instance.

        :param username: The username of the user.
        :param password: The password of the user.
        """
        self.__username = username
        self.__password = password
        self.__messages = []
        self.__is_active = False

    def update(self, massage: str):
        """
        Update the user with a new message.

        :param massage: The message to update the user with.
        """
        self.__messages.append(massage)
        print(f"get message: {massage}")

    def get_messages(self):
        """
        Get a copy of the user's messages.

        :return: A copy of the user's messages.
        """
        return copy.deepcopy(self.__messages)

    @abstractmethod
    def __str__(self):
        """
        Get the string representation of the user.

        :return: The string representation of the user.
        """
        pass

    def get_username(self):
        """
        Get the username of the user.

        :return: The username of the user.
        """
        return self.__username

    def logout(self):
        """
        Log the user out.
        """
        self.__is_active = False

    def login(self):
        """
        Log the user in.
        """
        self.__is_active = True

class Librarian(User):
    """
    A class representing a librarian, which is a type of user.
    """

    def __init__(self, username, password, inventory: Inventory.Inventory):
        """
        Initialize a new Librarian instance.

        :param username: The username of the librarian.
        :param password: The password of the librarian.
        :param inventory: The inventory managed by the librarian.
        """
        super().__init__(username, password)
        self.__inventory = inventory
        self.__inventory.add_subject(self)

    def add_book(self, book: Book):
        """
        Add a book to the inventory.

        :param book: The book to add.
        :return: The result of adding the book to the inventory.
        """
        return self.__inventory.add_to_inventory(book)

    def remove_book(self, book: Book):
        """
        Remove a book from the inventory.

        :param book: The book to remove.
        :return: The result of removing the book from the inventory.
        """
        return self.__inventory.remove_from_inventory(book)

    def search_book(self, search_strategy, query):
        """
        Search for a book in the inventory using a specified strategy.

        :param search_strategy: The strategy to use for searching (e.g., 'title', 'author').
        :param query: The query to search for.
        :return: The result of the search.
        :raises ValueError: If the search strategy is invalid.
        """
        switcher = {
            "title": Strategy.TitleSearch(),
            "author": Strategy.AuthorSearch(),
            "genre": Strategy.GenreSearch(),
            "year": Strategy.YearSearch(),
        }
        strategy = switcher.get(search_strategy.lower())
        if strategy:
            return strategy.search(self.__inventory.get_filter_books(), query)
        else:
            raise ValueError(f"Invalid search strategy: {search_strategy}")

    def add_user(self, user: User):
        """
        Add a user to the inventory's list of subjects.

        :param user: The user to add.
        """
        self.__inventory.add_subject(user)

    def remove_user(self, user: User):
        """
        Remove a user from the inventory's list of subjects.

        :param user: The user to remove.
        """
        self.__inventory.remove_user(user)

    def get_messages(self):
        """
        Get a copy of the librarian's messages.

        :return: A copy of the librarian's messages.
        """
        return super().get_messages()

    def get_popular_books(self):
        """
        Get the list of popular books from the inventory.

        :return: The list of popular books.
        """
        return self.__inventory.get_popular_books()

    def get_books(self):
        """
        Get the list of books from the inventory.

        :return: The list of books.
        """
        return self.__inventory.get_filter_books()

    def get_avilable(self):
        """
        Get the list of available books from the inventory.

        :return: The list of available books.
        """
        return self.__inventory.get_available_books()

    def loan_book(self, book: Book, info: str = ""):
        """
        Loan a book from the inventory.

        :param book: The book to loan.
        :param info: Additional information for the loan (default is an empty string).
        :return: The result of the loan operation.
        """
        return self.__inventory.loan_book(book, info)

    def return_book(self, book: Book):
        """
        Return a loaned book to the inventory.

        :param book: The book to return.
        :return: The result of the return operation.
        """
        return self.__inventory.return_book(book)

    def get_borrowed_books(self):
        """
        Get the list of borrowed books from the inventory.

        :return: The list of borrowed books.
        """
        return self.__inventory.get_borrowing_books()

    def update(self, massage: str):
        """
        Update the librarian with a new message.

        :param massage: The message to update the librarian with.
        """
        super().update(massage)
        print(f"get message: {massage}")

    def __str__(self):
        """
        Get the string representation of the librarian.

        :return: The string representation of the librarian.
        """
        return (f"Username: {self._User__username}, Password: {self._User__password}, "
                f"loan this books: got this messages: {self._User__messages}")

    def get_username(self):
        """
        Get the username of the librarian.

        :return: The username of the librarian.
        """
        return super().get_username()

    def __eq__(self, other):
        """
        Check if this librarian is equal to another librarian.

        :param other: The other librarian to compare with.
        :return: True if the librarians are equal, False otherwise.
        """
        return self.get_username() == other.get_username() and self.__password == other.__password

    def logout(self):
        """
        Log the librarian out.
        """
        self.is_active = False

    def login(self):
        """
        Log the librarian in.
        """
        self.is_active = True