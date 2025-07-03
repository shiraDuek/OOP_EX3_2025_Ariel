import unittest
import User
import Book
from Inventory import Inventory

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\033[1;31mstart test person class\033[0m")

    def setUp(self):
        self.inventory = Inventory()
        self.inventory.reset()
        self.p1 = User.Librarian("neriya", 1234, self.inventory)
        self.book1 = Book.Book("1984", "George Orwell", "Dystopian", 1949)
        self.book2 = Book.Book("War and Peace", "Leo Tolstoy", "Historical Fiction", 1869)
        self.book3 = Book.Book("The Catcher in the Rye", "J.D. Salinger", "Fiction", 1951)

    def test_add_book(self):
        result = self.p1.add_book(self.book1)
        self.assertTrue(result)
        self.assertIn(self.book1, self.inventory.get_filter_books())

    def test_remove_book(self):
        self.p1.add_book(self.book1)
        result = self.p1.remove_book(self.book1)
        self.assertTrue(result)
        self.assertNotIn(self.book1, self.inventory.get_filter_books())

    def test_search_book(self):
        self.p1.add_book(self.book1)
        result = self.p1.search_book("title", "1984")
        self.assertIn(self.book1, result)

    def test_add_user(self):
        user = User.Librarian("test_user", "password", self.inventory)
        self.p1.add_user(user)
        self.assertIn(user, self.inventory.Users)

    def test_get_popular_books(self):
        self.p1.add_book(self.book1)
        result = self.p1.get_popular_books()
        self.assertIn(self.book1, result)

    def test_get_books(self):
        self.p1.add_book(self.book1)
        result = self.p1.get_books()
        self.assertIn(self.book1, result)

    def test_get_avilable(self):
        self.p1.add_book(self.book1)
        result = self.p1.get_avilable()
        self.assertIn(self.book1, result)

    def test_loan_book(self):
        self.p1.add_book(self.book1)
        result = self.p1.loan_book(self.book1)
        self.assertEqual(result, 1)
        self.assertTrue(self.book1.is_all_loaned())

    def test_return_book(self):
        self.p1.add_book(self.book1)
        self.p1.loan_book(self.book1)
        result = self.p1.return_book(self.book1)
        self.assertTrue(result)
        self.assertFalse(self.book1.is_all_loaned())

    def test_get_borrowed_books(self):
        self.p1.add_book(self.book1)
        self.p1.loan_book(self.book1)
        self.p1.loan_book(self.book1)
        result = self.p1.get_borrowed_books()
        self.assertIn(self.book1, result)

if __name__ == '__main__':
    unittest.main()