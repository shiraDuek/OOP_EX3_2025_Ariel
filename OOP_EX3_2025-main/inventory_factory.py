from Book import Book

class Items:
    """
    A class representing different types of items.
    """
    BOOK = "book"

class Factory:
    """
    A factory class to create and add items to the inventory.
    """

    def __init__(self, inventory):
        """
        Initialize the Factory with an inventory.

        :param inventory: The inventory to add items to.
        """
        self.inventory = inventory

    def add_item(self, item: str, title, author, genre, year, copies=1, loan=False):
        """
        Add an item to the inventory.

        :param item: The type of item to add (e.g., 'book').
        :param title: The title of the item.
        :param author: The author of the item.
        :param genre: The genre of the item.
        :param year: The publication year of the item.
        :param copies: The number of copies of the item (default is 1).
        :param loan: The loan status of the item (default is False).
        """
        match item.lower():
            case Items.BOOK:
                try:
                    book = Book(title, author, genre, year, copies, loan)
                    self.inventory.add_to_inventory(book)
                except ValueError as e:
                    print(e)
            # open to add new items