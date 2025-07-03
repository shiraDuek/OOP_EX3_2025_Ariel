import unittest
from Book import Book
from Inventory import Inventory
from inventory_factory import Factory, Items

class TestFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\033[1;31mStart test factory class\033[0m")

    def setUp(self):
        self.inventory = Inventory()
        self.inventory.reset()
        self.factory = Factory(self.inventory)

    def test_add_book(self):
        self.factory.add_item(Items.BOOK, "1984", "George Orwell", "Dystopian", 1949, 2)
        books = list(self.inventory.get_filter_books().keys())
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].get_title(), "1984")
        self.assertEqual(books[0].get_author(), "George Orwell")
        self.assertEqual(books[0].get_genre(), "Dystopian")
        self.assertEqual(books[0].get_year(), 1949)
        self.assertEqual(books[0].get_total_copies(), 2)

    def test_add_book_invalid_genre(self):
        self.factory.add_item(Items.BOOK, "Animal Farm", "George Orwell", "Political Satire", 1945)

    def test_add_book_loan_status(self):
        self.factory.add_item(Items.BOOK, "Brave New World", "Aldous Huxley", "Science Fiction", 1932, 1, True)
        books = list(self.inventory.get_filter_books().keys())
        self.assertEqual(len(books), 1)
        self.assertTrue(books[0].is_all_loaned())

    def test_add_multiple_books(self):
        self.factory.add_item(Items.BOOK, "1984", "George Orwell", "Dystopian", 1949, 2)
        self.factory.add_item(Items.BOOK, "Animal Farm", "George Orwell", "Satire", 1945)
        books = list(self.inventory.get_filter_books().keys())
        self.assertEqual(len(books), 2)

    def test_add_book_default_copies(self):
        self.factory.add_item(Items.BOOK, "Animal Farm", "George Orwell", "Satire", 1945)
        books = list(self.inventory.get_filter_books().keys())
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].get_title(), "Animal Farm")
        self.assertEqual(books[0].get_total_copies(), 1)
        self.factory.add_item(Items.BOOK, "Animal Farm", "George Orwell", "Satire", 1945)
        self.assertEqual(books[0].get_total_copies(), 2)

    def test_add_book_multiple_copies(self):
        self.factory.add_item(Items.BOOK, "Animal Farm", "George Orwell", "Satire", 1945)
        books = list(self.inventory.get_filter_books().keys())
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].get_title(), "Animal Farm")
        self.assertEqual(books[0].get_total_copies(), 1)
        self.factory.add_item(Items.BOOK, "Animal Farm", "George Orwell", "Satire", 1945)
        self.assertEqual(books[0].get_total_copies(), 2)

if __name__ == "__main__":
    unittest.main()