import unittest
from Book import Book
from Gener import Genre

class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = Book("1984", "George Orwell", Genre.DYSTOPIAN, 1949, 2)

    def test_initialization(self):
        self.assertEqual(self.book.get_title(), "1984")
        self.assertEqual(self.book.get_author(), "George Orwell")
        self.assertEqual(self.book.get_genre(), "Dystopian")
        self.assertEqual(self.book.get_year(), 1949)
        self.assertEqual(self.book.get_total_copies(), 2)
        self.assertEqual(self.book.get_available_copies(), 2)
        self.assertFalse(self.book.is_all_loaned())

    def test_loan_book(self):
        self.assertTrue(self.book.loan())
        self.assertEqual(self.book.get_loaned_copies(), 1)
        self.assertEqual(self.book.get_available_copies(), 1)
        self.assertTrue(self.book.loan())
        self.assertEqual(self.book.get_loaned_copies(), 2)
        self.assertEqual(self.book.get_available_copies(), 0)
        self.assertFalse(self.book.loan())

    def test_return_book(self):
        self.book.loan()
        self.book.loan()
        self.assertTrue(self.book.return_loan())
        self.assertEqual(self.book.get_loaned_copies(), 1)
        self.assertEqual(self.book.get_available_copies(), 1)
        self.assertTrue(self.book.return_loan())
        self.assertEqual(self.book.get_loaned_copies(), 0)
        self.assertEqual(self.book.get_available_copies(), 2)
        self.assertFalse(self.book.return_loan())

    def test_equality(self):
        book2 = Book("1984", "George Orwell", Genre.DYSTOPIAN, 1949, 2)
        self.assertEqual(self.book, book2)
        self.assertFalse(self.book is book2)

    def test_invalid_initialization(self):
        with self.assertRaises(ValueError):
            Book("", "George Orwell", Genre.DYSTOPIAN, 1949)
        with self.assertRaises(ValueError):
            Book("1984", "", Genre.DYSTOPIAN, 1949)
        with self.assertRaises(ValueError):
            Book("1984", "George Orwell", "InvalidGenre", 1949)
        with self.assertRaises(ValueError):
            Book("1984", "George Orwell", Genre.DYSTOPIAN, 1949, -1)

if __name__ == '__main__':
    unittest.main()