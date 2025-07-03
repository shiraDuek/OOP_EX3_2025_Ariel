import unittest
from Book import Book
from Inventory import Inventory
import User


class TestInventory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\033[1;31mStart test inventory class\033[0m")

    def setUp(self):
        self.inventory = Inventory()
        self.inventory.reset()
        self.book1 = Book("1984", "George Orwell", "Dystopian", 1949, 2)
        self.book2 = Book("War and Peace", "Leo Tolstoy", "Historical Fiction", 1869, 3)
        self.book3 = Book("The Catcher in the Rye", "J.D. Salinger", "Fiction", 1951, 1)

    def tearDown(self):
        self.inventory.remove_from_inventory(self.book1)
        self.inventory.remove_from_inventory(self.book2)
        self.inventory.remove_from_inventory(self.book3)
        del self.inventory

    def test_add_to_inventory(self):
        self.inventory.add_to_inventory(self.book1)
        self.assertEqual(2, self.inventory.copies(self.book1))

    def test_remove_from_inventory(self):
        self.inventory.add_to_inventory(self.book1)
        self.assertTrue(self.inventory.remove_from_inventory(self.book1))
        self.assertEqual(0, self.inventory.copies(self.book1))

    def test_remove_from_inventory_loaned(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.loan_book(self.book1)
        self.assertFalse(self.inventory.remove_from_inventory(self.book1))

    def test_loan_book(self):
        self.inventory.add_to_inventory(self.book1)
        self.assertEqual(1, self.inventory.loan_book(self.book1, "user1"))
        self.assertEqual(1, self.inventory.loan_book(self.book1, "user2"))
        self.assertEqual(0, self.inventory.loan_book(self.book1, "user3"))

    def test_loan_book_not_in_inventory(self):
        self.assertEqual(-1, self.inventory.loan_book(self.book1, "user1"))

    def test_return_book(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.loan_book(self.book1, "user1")
        self.assertTrue(self.inventory.return_book(self.book1))
        self.assertEqual(2, self.inventory.copies(self.book1))

    def test_return_book_not_loaned(self):
        self.inventory.add_to_inventory(self.book1)
        self.assertFalse(self.inventory.return_book(self.book1))

    def test_copies(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.add_to_inventory(self.book2)
        self.assertEqual(2, self.inventory.copies(self.book1))
        self.assertEqual(3, self.inventory.copies(self.book2))

    def test_get_filter_books(self):
        self.inventory.add_to_inventory(self.book1)
        self.assertIn(self.book1, self.inventory.get_filter_books())

    def test_get_waiting_list(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.loan_book(self.book1, "user1")
        self.inventory.loan_book(self.book1, "user2")
        self.inventory.loan_book(self.book1, "user3")
        self.assertIn("user3", self.inventory.get_waiting_list()[self.book1])

    def test_reset(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.reset()
        self.assertEqual(0, self.inventory.copies(self.book1))

    def test_notify(self):
        user = User.Librarian("test_user", "password", self.inventory)
        self.inventory.add_subject(user)
        self.inventory.notify("test message")
        self.assertIn("test message", user.get_messages())

    def test_get_popular_books(self):
        # Add books to the inventory
        self.inventory.add_to_inventory(self.book1)
        self.inventory.add_to_inventory(self.book2)
        self.inventory.add_to_inventory(self.book3)

        # Loan some books
        self.inventory.loan_book(self.book1, "user1")
        self.inventory.loan_book(self.book1, "user2")
        self.inventory.loan_book(self.book2, "user3")

        # Add users to the waiting list
        self.inventory.add_to_waiting_list(self.book1, "user4")
        self.inventory.add_to_waiting_list(self.book2, "user5")

        # Get popular books
        popular_books = self.inventory.get_popular_books()

        # Check if the books are in the correct order
        self.assertEqual(popular_books[0], self.book1)
        self.assertEqual(popular_books[1], self.book2)
        self.assertEqual(popular_books[2], self.book3)

    def test_update_inventory_csv(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.update_inventory_csv()
        # Check if the CSV file is updated correctly
        with open(self.inventory.updated_csv_file, 'r') as file:
            content = file.read()
            self.assertIn("1984", content)

    def test_print_inventory(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.add_to_inventory(self.book2)
        self.inventory.print_inventory()
        # Check the printed output manually or redirect stdout to capture the output

    def test_print_waiting_list(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.loan_book(self.book1, "user1")
        self.inventory.loan_book(self.book1, "user2")
        self.inventory.loan_book(self.book1, "user3")
        self.inventory.print_waiting_list()
        # Check the printed output manually or redirect stdout to capture the output

    def test_str(self):
        self.inventory.add_to_inventory(self.book1)
        self.assertIn("1984", str(self.inventory))

    def test_get_available_books(self):
        self.inventory.add_to_inventory(self.book1)
        available_books = self.inventory.get_available_books()
        self.assertIn(self.book1, available_books)

    def test_get_borrowing_books(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.loan_book(self.book1, "user1")
        self.inventory.loan_book(self.book1, "user2")
        borrowing_books = self.inventory.get_borrowing_books()
        self.assertIn(self.book1, borrowing_books)

    def test_is_book_available(self):
        self.assertTrue(self.inventory.is_book_available("No"))
        self.assertFalse(self.inventory.is_book_available("Yes"))
        self.assertTrue(self.inventory.is_book_available("Borrowed: 1, Available: 1"))

    def test_is_book_borrowing(self):
        self.assertFalse(self.inventory.is_book_borrowing("No"))
        self.assertTrue(self.inventory.is_book_borrowing("Yes"))
        self.assertTrue(self.inventory.is_book_borrowing("Borrowed: 1, Available: 0"))

    def test_load_from_csv(self):
        self.inventory.load_from_csv('books.csv')
        # Check if the inventory is loaded correctly from the CSV file

    def test_save_to_csv(self):
        self.inventory.add_to_inventory(self.book1)
        self.inventory.save_to_csv('books.csv')
        # Check if the inventory is saved correctly to the CSV file

if __name__ == '__main__':
    unittest.main()