from abc import ABC, abstractmethod

import Inventory
from logger.Decorator import log_action

class Search(ABC):
    """
    Abstract base class for search strategies.
    This class defines a common interface for all search strategies.
    """
    @abstractmethod
    def search(self, inventory, query):
        """
        Abstract method to perform a search on the inventory.

        :param inventory: The inventory to search within.
        :param query: The search query.
        :return: List of search results.
        """
        pass

class TitleSearch(Search):
    """
    Concrete search strategy to search books by title.
    Implements the search method to find books by their title.
    """
    @log_action("Search book {title} by name completed", ["title"])
    def search(self, inventory, title):
        """
        Search for books by title.

        :param inventory: The inventory to search within.
        :param title: The title to search for.
        :return: List of books matching the title.
        """
        return [book for book in inventory if title.lower() in book.get_title().lower()]

class AuthorSearch(Search):
    """
    Concrete search strategy to search books by author.
    Implements the search method to find books by their author.
    """
    @log_action("Search book {author} by author completed", ["author"])
    def search(self, inventory, author):
        """
        Search for books by author.

        :param inventory: The inventory to search within.
        :param author: The author to search for.
        :return: List of books matching the author.
        """
        return [book for book in inventory if author.lower() in book.get_author().lower()]

class GenreSearch(Search):
    """
    Concrete search strategy to search books by genre.
    Implements the search method to find books by their genre.
    """
    def search(self, inventory, genre):
        """
        Search for books by genre.

        :param inventory: The inventory to search within.
        :param genre: The genre to search for.
        :return: List of books matching the genre.
        """
        return [book for book in inventory if genre.lower() in book.get_genre().lower()]

class YearSearch(Search):
    """
    Concrete search strategy to search books by year.
    Implements the search method to find books by their publication year.
    """
    def search(self, inventory, year):
        """
        Search for books by year.

        :param inventory: The inventory to search within.
        :param year: The year to search for.
        :return: List of books matching the year.
        """
        return [book for book in inventory if str(year) in str(book.get_year())]

if __name__ == "__main__":
    pass