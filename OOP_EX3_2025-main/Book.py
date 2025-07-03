from Gener import Genre

class Book:
    """
    A class representing a book in the inventory.
    """

    def __init__(self, title, author, genre, year, copies=1, loan=False):
        """
        Initialize a new Book instance.

        :param title: The title of the book.
        :param author: The author of the book.
        :param genre: The genre of the book.
        :param year: The publication year of the book.
        :param copies: The total number of copies available (default is 1).
        :param loan: The loan status of the book (default is False).
        :raises ValueError: If any of the parameters are invalid.
        """
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string.")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Author must be a non-empty string.")
        if not isinstance(copies, int) or copies <= 0:
            raise ValueError("Copies must be a positive integer.")

        if isinstance(genre, str):
            try:
                genre = Genre(genre)
            except ValueError:
                raise ValueError(f"Genre '{genre}' is invalid. Must be one of: {[g.value for g in Genre]}")

        if not isinstance(genre, Genre):
            raise ValueError(f"Genre must be one of: {[g.value for g in Genre]}")

        self.__title = title
        self.__author = author
        self.__total_copies = copies
        self.__genre = genre
        self.__year = year
        self.__loan = loan
        if loan == True:
            self.__loaned_copies = copies
        else:
            self.__loaned_copies = 0

    def set_total_copies(self, total_copies):
        """
        Set the total number of copies of the book.

        :param total_copies: The total number of copies.
        """
        self.__total_copies = total_copies

    def update_total_copies(self, additional_copies: int):
        """
        Update the total number of copies by adding additional copies.

        :param additional_copies: The number of additional copies to add.
        """
        if additional_copies > 0:
            self.__total_copies += additional_copies

    def get_loaned_copies(self):
        """
        Get the number of loaned copies of the book.

        :return: The number of loaned copies.
        """
        return self.__loaned_copies

    def get_title(self):
        """
        Get the title of the book.

        :return: The title of the book.
        """
        return self.__title

    def get_author(self):
        """
        Get the author of the book.

        :return: The author of the book.
        """
        return self.__author

    def get_genre(self):
        """
        Get the genre of the book.

        :return: The genre of the book.
        """
        return self.__genre.value

    def get_year(self):
        """
        Get the publication year of the book.

        :return: The publication year of the book.
        """
        return self.__year

    def get_total_copies(self):
        """
        Get the total number of copies of the book.

        :return: The total number of copies.
        """
        return self.__total_copies

    def get_available_copies(self):
        """
        Get the number of available copies of the book.

        :return: The number of available copies.
        """
        return self.__total_copies - self.__loaned_copies

    def is_all_loaned(self):
        """
        Check if all copies of the book are loaned out.

        :return: True if all copies are loaned out, False otherwise.
        """
        return self.__loaned_copies == self.__total_copies

    def loan(self):
        """
        Loan a copy of the book if available.

        :return: True if a copy was loaned, False otherwise.
        """
        if self.__loaned_copies < self.__total_copies:
            self.__loaned_copies += 1
            return True
        return False

    def get_availability(self):
        """
        Get the availability status of the book.

        :return: "Available" if there are copies available, "Not Available" otherwise.
        """
        return "Available" if self.get_available_copies() > 0 else "Not Available"

    def return_loan(self):
        """
        Return a loaned copy of the book.

        :return: True if a copy was returned, False otherwise.
        """
        if self.__loaned_copies > 0:
            self.__loaned_copies -= 1
            return True
        return False

    def __eq__(self, other):
        """
        Check if this book is equal to another book.

        :param other: The other book to compare with.
        :return: True if the books are equal, False otherwise.
        """
        if isinstance(other, Book):
            return (self.__title == other.__title and
                    self.__author == other.__author and
                    self.__genre == other.__genre and
                    self.__year == other.__year)
        return False

    def __hash__(self):
        """
        Get the hash value of the book.

        :return: The hash value of the book.
        """
        return hash((self.__title, self.__author, self.__genre, self.__year))

    def __str__(self):
        """
        Get the string representation of the book.

        :return: The string representation of the book.
        """
        loan_status = "yes" if self.__loan else "no"
        return (
            f"Title: '{self.__title}'\n"
            f"Author: {self.__author}\n"
            f"Year: {self.__year}\n"
            f"Genres: {self.get_genre()}\n"
            f"Status: {loan_status}\n"
        )

if __name__ == "__main__":
    pass