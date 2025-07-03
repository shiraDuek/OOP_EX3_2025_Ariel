import csv
from abc import ABC, abstractmethod
from copy import deepcopy
from logger.Decorator import log_action
import numpy as np
import pandas as pd
import Book


class Subject(ABC):
    """
    Abstract base class representing a subject in the observer pattern.
    """

    @abstractmethod
    def notify(self, subject):
        """
        Notify all observers about an event.

        :param subject: The subject to notify observers about.
        """
        pass

    @abstractmethod
    def add_subject(self, subject):
        """
        Add a subject to the list of subjects to be observed.

        :param subject: The subject to be added.
        """
        pass

class Inventory(Subject):
    __instance = None
    updated_csv_file = "books.csv"

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.Users = []
        if not hasattr(self, '_initialized'):
            self.__filter_book = {}
            self.__waiting_list = {}
            self._initialized = True
        self._iter_index = 0
        self._books_list = list(self.__filter_book.keys())

    def __iter__(self):
        """
        Initialize the iterator.
        """
        self._iter_index = 0
        self._books_list = list(self.__filter_book.keys())
        return self

    def __next__(self):
        """
        Return the next book in the inventory.
        """
        if self._iter_index < len(self._books_list):
            book = self._books_list[self._iter_index]
            self._iter_index += 1
            return book
        else:
            raise StopIteration

    def update_inventory_csv(self):
        """
        Save the current inventory to the CSV file.
        """
        try:
            self.save_to_csv(self.updated_csv_file)
        except Exception as e:
            print(f"Error updating inventory CSV: {e}")

    def add_to_inventory(self, book: Book.Book):
        """
        Add a book to the inventory.
        """
        if book in self.__filter_book:
            existing_copies = len(self.__filter_book[book])
            if book.get_total_copies() == existing_copies:
                for _ in range(book.get_total_copies()):
                    self.__filter_book[book].append(deepcopy(book))
                book.update_total_copies(book.get_total_copies())
            else:
                for i in range(book.get_total_copies()):
                    self.__filter_book[book].append(deepcopy(book))
        else:
            self.__filter_book[book] = [deepcopy(book) for i in range(book.get_total_copies())]

        if book not in self.__waiting_list:
            self.__waiting_list[book] = []

        self.update_inventory_csv()
        return True

    @log_action("book removed")
    def remove_from_inventory(self, book: Book.Book):
        """
        Remove a book from the inventory.
        """
        for key, books in self.__filter_book.items():
            if key.get_title() == book.get_title() and key.get_author() == book.get_author() and key.get_year() == book.get_year() and key.get_genre() == book.get_genre():
                if key.get_available_copies() == key.get_total_copies():
                    del self.__filter_book[book]
                    self.update_inventory_csv()
                    return True
        return False

    @log_action("book borrowed")
    def loan_book(self, book: Book, info: str = ""):
        """
        Loan a book from the inventory.
        """
        for key, books in self.__filter_book.items():
            if key.get_title() == book.get_title() and key.get_author() == book.get_author() and key.get_year() == book.get_year() and key.get_genre() == book.get_genre():

                if key.loan():
                    self.update_inventory_csv()
                    return 1
                return self.add_to_waiting_list(book, info)
        return -1

    def add_to_waiting_list(self, book: Book, info: str):
        """
        Add a user to the waiting list for a book.
        """
        for key, books in self.__filter_book.items():
            if key.get_title() == book.get_title() and key.get_author() == book.get_author():
                if key not in self.__waiting_list:
                    self.__waiting_list[key] = []
                if info not in self.__waiting_list[key]:
                    self.__waiting_list[key].append(info)
                self.update_inventory_csv()
                return 0
        return -1

    @log_action("book returned")
    def return_book(self, book: Book):
        """
        Return a borrowed book to the inventory.
        """
        for key, books in self.__filter_book.items():
            if key.get_title() == book.get_title() and key.get_author() == book.get_author() and key.get_year() == book.get_year() and key.get_genre() == book.get_genre():
                if key.return_loan() is True:
                    if book in self.__waiting_list and self.__waiting_list[book]:
                        next_user = self.__waiting_list[book].pop(0)
                        for s in self.Users:
                            s.update(f"Book {book.get_title()} by {book.get_author()} is available for {next_user}")
                        key.loan()
                        if not self.__waiting_list[book]:
                            del self.__waiting_list[book]
                            for s in self.Users:
                                s.update(f"Book {book.get_title()} by {book.get_author()} is available")
                    self.update_inventory_csv()
                    return True
        return False

    def copies(self, book: Book.Book):
        """
        Return the total number of copies of a book in the inventory.
        """
        total_copies = 0
        for books in self.__filter_book.values():
            for b in books:
                if (b.get_title() == book.get_title() and
                        b.get_author() == book.get_author() and
                        b.get_year() == book.get_year() and
                        b.get_genre() == book.get_genre()):
                    total_copies += 1
        return total_copies

    def return_total_copies(self):
        """
        Return a dictionary with the total number of copies for each book.
        """
        total_copies = {}
        for books in self.__filter_book.values():
            for book in books:
                title = book.get_title()
                if title in total_copies:
                    total_copies[title] += 1
                else:
                    total_copies[title] = 1

        return total_copies

    def print_inventory(self):
        """
        Print the inventory of books.
        """
        for key, value in self.__filter_book.items():
            print(
                f"{{'{key.get_title()}' by {key.get_author()} ({key.get_year()}) - {key.get_genre()}: "
                f"[{', '.join(str(book) for book in value)}]}}")

    def print_waiting_list(self):
        """
        Print the waiting list for books.
        """
        for key, value in self.__waiting_list.items():
            print(
                f"{{'{key.get_title()}' by {key.get_author()} ({key.get_year()}) - {key.get_genre()}: "
                f"[{', '.join(str(book) for book in value)}]}}")

    def __str__(self):
        """
        Return a string representation of the inventory.
        """
        return ", ".join(
            f"{{'{key.get_title()}' by {key.get_author()} ({key.get_year()}) - {key.get_genre()}: "
            f"[{', '.join(str(book) for book in value)}]}}"
            for key, value in self.__filter_book.items()
        )

    def get_filter_books(self):
        """
        Return the dictionary of books and their copies.
        """
        return self.__filter_book

    def get_waiting_list(self):
        """
        Return the waiting list dictionary.
        """
        return self.__waiting_list

    def get_available_books(self):
        """
        Return a list of available books.
        """
        try:
            df = pd.read_csv(self.updated_csv_file)

            available_books = df[df['is_loaned'].apply(self.is_book_available)]

            available_books_list = [
                Book.Book(
                    title=str(row['title']),
                    author=row['author'],
                    year=row['year'],
                    genre=row['genre']
                ) for _, row in available_books.iterrows()
            ]
            return available_books_list

        except Exception as e:
            print(f"Error loading available books: {e}")
            return []

    def get_borrowing_books(self):
        """
        Return a list of borrowed books, book is borrowed iff all of his copies are loaned.
        """
        try:
            df = pd.read_csv(self.updated_csv_file)

            borrowing_books = df[df['is_loaned'].apply(self.is_book_borrowing)]

            borrowing_books_list = [
                Book.Book(
                    title=str(row['title']),
                    author=row['author'],
                    year=row['year'],
                    genre=row['genre']
                ) for _, row in borrowing_books.iterrows()
            ]
            return borrowing_books_list

        except Exception as e:
            print(f"Error loading borrowing books: {e}")
            return []

    def is_book_available(self, loan_status):
        """
        Check if a book is available based on its loan status.
        """
        if loan_status == 'No':
            return True

        if loan_status.startswith("Borrowed:"):
            available_books_count = int(loan_status.split("Available: ")[1])
            return available_books_count > 0

        return False

    def is_book_borrowing(self, loan_status):
        """
        Check if a book is currently borrowed based on its loan status.
        """
        if loan_status == 'Yes':
            return True

        if loan_status.startswith("Borrowed:"):
            borrowed_books_count = int(loan_status.split("Borrowed: ")[1].split(",")[0])
            available_books_count = int(loan_status.split("Available: ")[1])
            return borrowed_books_count > 0 and available_books_count == 0

        return False

    def load_from_csv(self, file_path):
        """
        Load books from a CSV file into the inventory.
        """
        try:
            df = pd.read_csv(file_path)
            if 'waiting_list' in df.columns:
                for _, row in df.iterrows():
                    book = Book.Book(
                        title=row['title'],
                        author=row['author'],
                        genre=row['genre'],
                        year=row['year'],
                    )
                    total_copies = row['copies']
                    book.set_total_copies(total_copies)

                    loan_status = row['is_loaned']
                    if loan_status == "Yes":
                        for _ in range(total_copies):
                            book.loan()
                    elif loan_status.startswith("Borrowed:"):
                        borrowed = int(loan_status.split("Borrowed: ")[1].split(",")[0])
                        available = total_copies - borrowed
                        for _ in range(borrowed):
                            book.loan()

                    waiting_list = row['waiting_list']
                    if pd.isna(waiting_list):
                        self.__waiting_list[book] = []
                    else:
                        self.__waiting_list[book] = waiting_list.split('\n')

                    self.add_to_inventory(deepcopy(book))
            else:
                for _, row in df.iterrows():
                    book = Book.Book(
                        title=row['title'],
                        author=row['author'],
                        loan=(row['is_loaned'].strip().lower() == 'yes'),
                        copies=row['copies'],
                        genre=row['genre'],
                        year=row['year'],
                    )
                    self.add_to_inventory(deepcopy(book))
        except Exception as e:
            print(f"Error loading books from CSV: {e}")

    def save_to_csv(self, file_path):
        """
        Save the current inventory to a CSV file.
        """
        data = []
        total_copies_dict = self.return_total_copies()
        processed_titles = set()

        for book, copies in self.__filter_book.items():
            title = book.get_title()

            if title in processed_titles:
                continue

            processed_titles.add(title)

            total_copies = total_copies_dict.get(title)
            book.set_total_copies(total_copies)
            borrowed = book.get_loaned_copies()
            available = book.get_available_copies()

            if borrowed == total_copies:
                loan_status = "Yes"
            elif available == total_copies:
                loan_status = "No"
            else:
                loan_status = f"Borrowed: {borrowed}, Available: {available}"

            waiting_list = '\n'.join(self.__waiting_list.get(book, [])) if self.__waiting_list.get(book) else "None"

            data.append({
                "title": title,
                "author": book.get_author(),
                "genre": book.get_genre(),
                "year": book.get_year(),
                "copies": total_copies,
                "is_loaned": loan_status,
                "waiting_list": waiting_list
            })

        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

    def notify(self, message):
        """
        Notify all users with a message.
        """
        for user in self.Users:
            user.update(message)

    def add_subject(self, subject):
        """
        Add a user to the list of users to be notified.
        """
        self.Users.append(subject)

    def remove_user(self, user):
        """
        Remove a user from the list of users to be notified.
        """
        self.Users.remove(user)

    def reset(self):
        """
        Reset the inventory and waiting list, and clear the CSV file (mostly for test).
        """
        self.__filter_book.clear()
        self.__waiting_list.clear()
        pd.DataFrame(
            columns=["title", "author", "genre", "year", "total_copies", "loan_status", "waiting_list"]).to_csv(
            self.updated_csv_file, index=False)

    def get_popular_books(self):
        """
        Return a list of popular books based on the number of loans and waiting list count.
        """
        popular_books = []

        for book, copies in self.__filter_book.items():
            total_lend_copies = book.get_loaned_copies()
            waiting_list_count = len(self.__waiting_list.get(book, []))
            popularity_score = total_lend_copies + waiting_list_count

            popular_books.append((book, popularity_score))

        popular_books.sort(key=lambda x: x[1], reverse=True)
        return [book for book, score in popular_books]


if __name__ == "__main__":
    pass

