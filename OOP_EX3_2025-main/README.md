# Library Management System

## Overview
This project is a Library Management System built using Python and Tkinter for the GUI. It allows users to manage books, including adding, removing, searching, borrowing, and returning books. The system also supports searching books by genre and logging actions.

## Features
- Add, remove, search, borrow, and return books.
- Search books by title, author, genre, and year.
- View all books and borrowed books.
- Log actions for tracking user activities.

## Design Patterns
- **Strategy Pattern**: Used for different search strategies (`TitleSearch`, `AuthorSearch`, `GenreSearch`, `YearSearch`).
- **Decorator Pattern**: Used for logging actions (`log_action` decorator).
- **Factory Pattern**: Used for creating an Inventory object (`Inventory_Factory`).
- **Singleton Pattern**: Used for the `Inventory` class to connect every user to the same inventory.
- **Observer Pattern**: Used for the `User` class to notify users when a book is borrowed or returned.
- **Iterator Pattern**: Used for iterating over the books in the inventory.

## System Architecture
The system consists of the following classes:
- **Book**: Represents a book with title, author, genre, and year.
- **Inventory**: Represents a library Inventory with a list of books and borrowed books (the main library functionality).
- **Search**: Interface for search strategies.
- **GenreSearch**, **TitleSearch**, **AuthorSearch**, **YearSearch**: Concrete search strategies (using strategy design pattern).
- **Logger**: Logs actions for tracking user activities (using decorator design pattern).
- **LibraryGUI**: GUI for the Library Management System.
- **User**: Represents a user with a name and password.
- **UserManager**: Manages users and their actions.
- **Inventory_Factory**: Factory for creating an Inventory object (open for add more different items and functionality).
- **BookIterator**: Iterator for iterating over the books in the inventory.
- **Observer**: Observer for notifying users when a book is borrowed or returned.
- **Subject**: Subject for notifying observers when a book is borrowed or returned.

## Prerequisites
- Python 3.8 or higher
- Tkinter (usually included with Python)
- `ttk` module for advanced widgets
- `messagebox` for displaying messages
- `pandas` for reading and writing CSV files
- `werkzeug` for password hashing
- `unittest` for testing
- `numpy` for numerical operations
- `logging` for logging actions


## Installation
1. Clone the repository:
  ```bash
   git clone https://github.com/NeriyaFilber/OOP_EX3_2025.git
   ```
2. Run the `libraryGUI.py` file:
  ```bash
   python LibraryGui.py
   ```


## Testing
The system have been tested using the `unittest` module. The tests can be found in the `tests` directory.
To run all the tests at once, run the `test_runner.py` file or run the following command:
```bash
python -m unittest discover tests
```

## Necessary installation
To run the project you need to install the following packages:
```bash
pip install unittest
```
```bash
pip install tkinter
```
```bash
pip install pandas
```
```bash
pip install numpy
```
```bash
pip install werkzeug
```

Now all you need to do is run the `LibraryGUI.py` file and enjoy the project.

## Authors
- Neriya Filber
- Shira Duek

   