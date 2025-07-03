from unittest import TestCase
from Book import Book
from Inventory import Inventory
import Search.Strategy

class TestSearch(TestCase):

    @classmethod
    def setUpClass(cls):
        print("\033[1;31mStart test search class\033[0m")

    def setUp(self):
        # Create inventory and add books
        self.inventory = Inventory()
        self.inventory.reset()
        self.book1 = Book("1984", "George Orwell", "Dystopian", 1949, 2)
        self.book2 = Book("War and Peace", "Leo Tolstoy", "Historical Fiction", 1869, 3)
        self.book3 = Book("The Catcher in the Rye", "J.D. Salinger Leo", "Fiction", 1951, 1)
        self.book4 = Book("1984 ed", "J.D. Salinger", "Fiction", 1951, 1)

        self.inventory.add_to_inventory(self.book1)
        self.inventory.add_to_inventory(self.book2)
        self.inventory.add_to_inventory(self.book3)
        self.inventory.add_to_inventory(self.book4)

    def test_title_search(self):
        title_search = Search.Strategy.TitleSearch()
        result = title_search.search(self.inventory, '19')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].get_title(), "1984")

        result = title_search.search(self.inventory, 'e')
        self.assertEqual(len(result), 3)

    def test_author_search(self):
        author_search = Search.Strategy.AuthorSearch()
        result = author_search.search(self.inventory, "Leo")
        self.assertEqual(len(result), 2)

    def test_year_search(self):
        year_search = Search.Strategy.YearSearch()
        result = year_search.search(self.inventory, '19')
        self.assertEqual(len(result), 3)

    def test_genre_search(self):
        genre_search = Search.Strategy.GenreSearch()
        result = genre_search.search(self.inventory, 'Ficti')
        self.assertEqual(len(result), 3)