import os
import tkinter as tk
from tkinter import messagebox, ttk
import Book
import Search.Strategy
from Gener import Genre
from Inventory import Inventory
from User import User

from UserManagement import UserManagement
from logger.Decorator import log_action


class GUI:
    def __init__(self):

        self.library_inventory = Inventory()
        self.user = None

        initial_csv_file = "books.csv"


        self.library_inventory.load_from_csv(initial_csv_file)
        print("Books loaded successfully from initial CSV.")
        print("Books loaded successfully from CSV.")
        self.user_management = UserManagement()
        self.root = tk.Tk()
        self.root.title("Library System")
        self.root.geometry("1200x600")
        self.root.resizable(False, False)
        self.init_login_ui()

    def show_login(self):
        self.clear_ui()
        self.init_login_ui()
    def show_register(self):
        self.clear_ui()
        self.init_register_ui()
    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def back(self):
        self.clear_ui()
        self.init_after_login_ui()
    @log_action("registered")
    def register_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        if username and password:
            if self.user_management.user_exists(username):
                messagebox.showerror("Error",
                                     f"Username '{username}' already exists. Please choose a different username.")
                return False
            else:
                self.user_management.add_user(username, password)
                messagebox.showinfo("Registration Successful", f"User '{username}' registered successfully.")

                self.show_login()
                return True
        else:
            messagebox.showerror("Error", "Both fields are required.")
            return False

    @log_action("logged in")
    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_management.authenticate_user(username, password):
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            mange = UserManagement()
            self.user = mange.get_user_from_csv(username)
            self.user.login()
            self.init_after_login_ui()
            return True
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return False
    def init_login_ui(self):
        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=10)

        tk.Label(login_frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(login_frame, text="Login", command=self.login_user).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(login_frame, text="Register", command=self.show_register).grid(row=3, column=0, columnspan=2, pady=5)
    def init_register_ui(self):
        register_frame = tk.Frame(self.root)
        register_frame.pack(pady=10)

        tk.Label(register_frame, text="New Username:").grid(row=0, column=0, pady=5)
        self.reg_username_entry = tk.Entry(register_frame)
        self.reg_username_entry.grid(row=0, column=1, pady=5)

        tk.Label(register_frame, text="New Password:").grid(row=1, column=0, pady=5)
        self.reg_password_entry = tk.Entry(register_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, pady=5)

        tk.Button(register_frame, text="Register", command=self.register_user).grid(row=2, column=0, columnspan=2,
                                                                                    pady=10)
        tk.Button(register_frame, text="Back to Login", command=self.show_login).grid(row=3, column=0, columnspan=2,
                                                                                      pady=5)
    def init_after_login_ui(self):
        self.clear_ui()
        tk.Label(self.root, text="Possible Actions", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Add Book", command=self.gui_add_book).pack(pady=5)
        tk.Button(self.root, text="Remove Book", command=self.gui_remove_book).pack(pady=5)
        tk.Button(self.root, text="Search Book", command=self.create_main_search_window).pack(pady=5)
        tk.Button(self.root, text="View Books", command=self.gui_view_book).pack(pady=5)
        tk.Button(self.root, text="Lend Books", command=self.gui_loan_book).pack(pady=5)
        tk.Button(self.root, text="Return Books", command=self.gui_return_book).pack(pady=5)
        tk.Button(self.root, text="popular Books", command=self.gui_popular_book).pack(pady=5)
        tk.Button(self.root, text="Search by Genre", command=self.open_genre_search_window).pack(pady=5)  # New button
        tk.Button(self.root, text="Logout", command=self.gui_logout).pack(pady=5)

    @log_action("log out")
    def gui_logout(self):
        self.user.logout()
        self.user = None
        self.clear_ui()
        self.init_login_ui()
        return True
    def gui_add_book(self):
        self.clear_ui()
        tk.Label(self.root, text="Add a New Book", font=("Arial", 16)).pack(pady=10)

        self.title_entry = self.create_input_field("Title")
        self.author_entry = self.create_input_field("Author")
        self.gener_entry = self.create_input_field("Gener")
        self.year_entry = self.create_input_field("Year")

        tk.Button(self.root, text="Add Book", command=self.add_book_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def gui_remove_book(self):
        self.clear_ui()
        tk.Label(self.root, text="Remove a Book", font=("Arial", 16)).pack(pady=10)

        self.title_entry = self.create_input_field("Title")
        self.author_entry = self.create_input_field("Author")


        tk.Button(self.root, text="Remove Book", command=self.remove_book_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def gui_view_book(self):
        self.clear_ui()
        tk.Label(self.root, text="View Books", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="View All Books", command=self.show_books_action).pack(pady=5)
        tk.Button(self.root, text="View Available Books", command=self.show_available_books_action).pack(pady=5)
        tk.Button(self.root, text="View Borrowed Books", command=self.show_borrowed_books_action).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def gui_loan_book(self):
        self.clear_ui()
        tk.Label(self.root, text="Loan Book", font=("Arial", 16)).pack(pady=10)

        self.title_entry = self.create_input_field("Title")
        self.author_entry = self.create_input_field("Author")


        tk.Button(self.root, text="Loan Book", command=self.loan_book_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def gui_return_book(self):
        self.clear_ui()
        tk.Label(self.root, text="return Book", font=("Arial", 16)).pack(pady=10)

        self.title_entry = self.create_input_field("Title")
        self.author_entry = self.create_input_field("Author")

        tk.Button(self.root, text="return Book", command=self.return_book_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def create_input_field(self, label):
        tk.Label(self.root, text=label + ":").pack(anchor="w", padx=20)
        entry = tk.Entry(self.root)
        entry.pack(padx=20)
        return entry

    @log_action("displayed")
    def gui_popular_book(self):
        self.clear_ui()
        tk.Label(self.root, text="Popular Books", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.pack(pady=10)

        books = self.user.get_popular_books()
        for book in books:
            self.tree.insert("", "end", values=(book.get_title(), book.get_author(), book.get_year(), book.get_genre()))

        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
        return bool(books)

    @log_action("book added")
    def add_book_action(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        category = self.gener_entry.get()
        year = self.year_entry.get()

        if not title or not author or not category or not year:
            messagebox.showerror("Error", "All fields are required.")
            return False

        if not year.isdigit() :
            messagebox.showerror("Error", "Year must be a digit number.")
            return False

        if not isinstance(category, str):
            messagebox.showerror("Error", "Category must be a string.")
            return False

        valid_categories = [g.value for g in Genre]
        if category not in valid_categories:
            messagebox.showerror("Error", f"Genre '{category}' is invalid. Must be one of: {valid_categories}")
            return False

        new_book = Book.Book(title, author, category, year)
        if self.user.add_book(book=new_book):
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.back()
            return True
        else:
            messagebox.showerror("Failed", f"Failed to add book '{title}'.")
            return True
    def remove_book_action(self):
        title = self.title_entry.get()
        author = self.author_entry.get()

        if not (title and author):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        title_search = Search.Strategy.TitleSearch()
        author_search = Search.Strategy.AuthorSearch()

        books_by_title = title_search.search(self.user.get_books(), title)

        books_by_author = author_search.search(books_by_title, author)

        if not books_by_author:
            messagebox.showerror("Error", f"The book '{title}' by {author} does not exist in the inventory.")
            return

        self.display_results_in_tree_remove(books_by_author)
    def create_main_search_window(self):
        self.clear_ui()
        tk.Label(self.root, text="Search Options", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Search by Title", command=self.open_title_search).pack(pady=5)
        tk.Button(self.root, text="Search by Author", command=self.open_author_search).pack(pady=5)
        tk.Button(self.root, text="Search by Genre", command=self.open_genre_search).pack(pady=5)
        tk.Button(self.root, text="Search by Year", command=self.open_year_search).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def open_title_search(self):
        self.clear_ui()
        tk.Label(self.root, text="Search by Title", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Enter Title:").pack(pady=5)
        title_entry = tk.Entry(self.root)
        title_entry.pack(pady=5)

        tk.Button(self.root, text="Search", command=lambda: self.search_by_title(title_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_search_window).pack(pady=10)
    def search_by_title(self, title):
        if not title:
            messagebox.showerror("Error", "Please enter a title to search.")
            return
        results = self.user.search_book("title",title)
        if not results:
            messagebox.showinfo("No Results", f"No books found")
            return
        self.display_results_in_tree(results)
    def open_author_search(self):
        self.clear_ui()
        tk.Label(self.root, text="Search by Author", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Enter Author:").pack(pady=5)
        author_entry = tk.Entry(self.root)
        author_entry.pack(pady=5)

        tk.Button(self.root, text="Search", command=lambda: self.search_by_author(author_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_search_window).pack(pady=10)
    def search_by_author(self, author):
        if not author:
            messagebox.showerror("Error", "Please enter an author to search.")
            return
        results = self.user.search_book("author",author)

        if not results:
            messagebox.showinfo("No Results", f"No books found")
            return
        self.display_results_in_tree(results)
    def open_genre_search(self):
        self.clear_ui()
        tk.Label(self.root, text="Search by Genre", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Enter Genre:").pack(pady=5)
        genre_entry = tk.Entry(self.root)
        genre_entry.pack(pady=5)

        tk.Button(self.root, text="Search", command=lambda: self.search_by_genre(genre_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_search_window).pack(pady=10)
    def search_by_genre(self, genre):
        if not genre:
            messagebox.showerror("Error", "Please enter a genre to search.")
            return
        results = self.user.search_book("genre", genre)
        if not results:
            messagebox.showinfo("No Results", f"No books found")
            return
        self.display_results_in_tree(results)
    def open_year_search(self):
        self.clear_ui()
        tk.Label(self.root, text="Search by Year", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Enter Year:").pack(pady=5)
        year_entry = tk.Entry(self.root)
        year_entry.pack(pady=5)

        tk.Button(self.root, text="Search", command=lambda: self.search_by_year(year_entry.get())).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_search_window).pack(pady=10)
    def search_by_year(self, year):
        if not year:
            messagebox.showerror("Error", "Please enter a year to search.")
            return

        try:
            year_value = int(year)
            results = self.user.search_book("year", year_value)

            if not results:
                messagebox.showinfo("No Results", f"No books found")
                return


            self.display_results_in_tree(results)
        except ValueError:
            messagebox.showerror("Error", "Year must be a number.")
    def display_results_in_tree(self, results):
        self.clear_ui()
        tk.Label(self.root, text="Search Books", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre", "Availability"),
                                 show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Availability", text="Availability")
        self.tree.pack(pady=10)
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not results:
            messagebox.showinfo("No Results", "No books found matching the criteria.")
            self.tree.pack_forget()
            return

        for book in results:
            self.tree.insert("", "end", values=(
                book.get_title(),
                book.get_author(),
                book.get_year(),
                book.get_genre(),
                book.get_availability()
            ))
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def display_results_in_tree_loan(self, results):
        self.clear_ui()
        tk.Label(self.root, text="Book list", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Click twice on the wanted book below").pack(pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre", "Availability"),
                                 show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Availability", text="Availability")
        self.tree.pack(pady=10)
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not results:
            messagebox.showinfo("No Results", "No books found matching the criteria.")
            self.tree.pack_forget()
            return

        for book in results:
            self.tree.insert("", "end", values=(
                book.get_title(),
                book.get_author(),
                book.get_year(),
                book.get_genre(),
                book.get_availability()
            ))
        self.tree.bind("<Double-1>", self.on_book_select)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def display_results_in_tree_remove(self, results):
        self.clear_ui()
        tk.Label(self.root, text="Book list", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Click twice on the wanted book below").pack(pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre", "Availability"),
                                 show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Availability", text="Availability")
        self.tree.pack(pady=10)
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not results:
            messagebox.showinfo("No Results", "No books found matching the criteria.")
            self.tree.pack_forget()
            return

        for book in results:
            self.tree.insert("", "end", values=(
                book.get_title(),
                book.get_author(),
                book.get_year(),
                book.get_genre(),
                book.get_availability()
            ))
        self.tree.bind("<Double-1>", self.remove_book_select)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def remove_book_select(self, event):
        selected_item = self.tree.selection()[0]
        book_details = self.tree.item(selected_item, "values")
        title, author, year, genre, availability = book_details
        self.clear_ui()
        tk.Label(self.root, text=f"remove Book: {title} by {author}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Remove Book", command=lambda: self.finalize_remove(book_details)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def display_results_in_tree_return(self, results):
        self.clear_ui()
        tk.Label(self.root, text="Book list", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Click twice on the wanted book below").pack(pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre", "Availability"),
                                 show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Availability", text="Availability")
        self.tree.pack(pady=10)
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not results:
            messagebox.showinfo("No Results", "No books found matching the criteria.")
            self.tree.pack_forget()
            return

        for book in results:
            self.tree.insert("", "end", values=(
                book.get_title(),
                book.get_author(),
                book.get_year(),
                book.get_genre(),
                book.get_availability()
            ))
        self.tree.bind("<Double-1>", self.re_book_select)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def on_book_select(self, event):
        selected_item = self.tree.selection()[0]
        book_details = self.tree.item(selected_item, "values")
        title, author, year, genre, availability = book_details


        self.clear_ui()
        tk.Label(self.root, text=f"Loan Book: {title} by {author}", font=("Arial", 16)).pack(pady=10)

        self.full_name = self.create_input_field("Full Name")
        self.phone = self.create_input_field("Phone")
        self.email = self.create_input_field("Email")

        tk.Button(self.root, text="Loan Book", command=lambda: self.finalize_loan(book_details)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def finalize_loan(self, book_details):
        title, author, year, genre, availability = book_details

        full_name = self.full_name.get()
        phone = self.phone.get()
        email = self.email.get()

        if not (full_name and phone and email):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        _book = Book.Book(title, author, genre, int(year))

        contact_info = f"{full_name}\t{phone}\t{email}"
        result = self.user.loan_book(_book, contact_info)

        if result == 1:
            messagebox.showinfo("Success", f"The book '{title}' by {author} has been successfully loaned.")
        elif result == 0:
            messagebox.showinfo("Waitlist", f"The book '{title}' by {author} is currently on the waitlist.")
        else:
            messagebox.showerror("Error", f"The book '{title}' by {author} is not available for loan.")

    @log_action("Displayed all books")
    def show_books_action(self):
        self.clear_ui()
        tk.Label(self.root, text="All Books", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.pack(pady=10)

        books = self.user.get_books()
        for book in books:
            self.tree.insert("", "end", values=(book.get_title(), book.get_author(), book.get_year(), book.get_genre()))

        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
        return bool(books)

    @log_action("Displayed available books")
    def show_available_books_action(self):
        self.clear_ui()
        tk.Label(self.root, text="Available Books", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.pack(pady=10)

        books = self.user.get_avilable()
        for book in books:
            self.tree.insert("", "end", values=(book.get_title(), book.get_author(), book.get_year(), book.get_genre()))

        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
        return bool(books)

    @log_action("Displayed borrowed books")
    def show_borrowed_books_action(self):
        self.clear_ui()
        tk.Label(self.root, text="Borrowed Books", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.pack(pady=10)

        books = self.user.get_borrowed_books()
        for book in books:
            self.tree.insert("", "end", values=(book.get_title(), book.get_author(), book.get_year(), book.get_genre()))

        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
        return bool(books)

    def loan_book_action(self):
        title = self.title_entry.get()
        author = self.author_entry.get()

        if not (title and author):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        try:

            title_search = Search.Strategy.TitleSearch()
            author_search = Search.Strategy.AuthorSearch()

            books_by_title = title_search.search(self.user.get_books(), title)

            books_by_author = author_search.search(books_by_title, author)

            if not books_by_author:
                messagebox.showerror("Error", f"The book '{title}' by {author} does not exist in the inventory.")
                return

            self.display_results_in_tree_loan(books_by_author)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    def re_book_select(self, event):
        selected_item = self.tree.selection()[0]
        book_details = self.tree.item(selected_item, "values")
        title, author, year, genre, availability = book_details


        self.clear_ui()
        tk.Label(self.root, text=f"return Book: {title} by {author}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Return Book", command=lambda: self.finalize_return(book_details)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    def finalize_return(self, book_details):
        title, author, year, genre, availability = book_details

        _book = Book.Book(title, author, genre, int(year))

        result = self.user.return_book(_book)

        if result:
            messagebox.showinfo("Success", f"The book '{title}' by {author} has been successfully returned.")
        else:
            messagebox.showerror("Error",
                                 f"The book '{title}' by {author} could not be returned. It may not have been loaned out.")
    def finalize_remove(self, book_details):
        title, author, year, genre, availability = book_details

        _book = Book.Book(title, author, genre, int(year))

        result = self.user.remove_book(_book)

        if result:
            messagebox.showinfo("Success", f"Book '{title}' removed successfully!")
            self.back()
        else:
            messagebox.showerror("Failed", f"Failed to remove book '{title}'.")
    def return_book_action(self):
        title = self.title_entry.get()
        author = self.author_entry.get()

        if not (title and author):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        try:
            title_search = Search.Strategy.TitleSearch()
            author_search = Search.Strategy.AuthorSearch()
            books_by_title = title_search.search(self.user.get_books(), title)

            books_by_author = author_search.search(books_by_title, author)

            if not books_by_author:
                    messagebox.showerror("Error", f"The book '{title}' by {author} does not exist in the inventory.")
                    return

            self.display_results_in_tree_return(books_by_author)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def open_genre_search_window(self):
        self.clear_ui()
        tk.Label(self.root, text="Search by Genre", font=("Arial", 16)).pack(pady=10)

        genre_frame = tk.Frame(self.root)
        genre_frame.pack(pady=10)

        for genre in Genre:
            tk.Button(genre_frame, text=genre.value, command=lambda g=genre: self.search_by_genre_without_permutation(g.value)).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.back).pack(pady=10)
    @log_action("Displayed book by category")
    def filter_books_by_genre(self, genre):
        all_books = self.user.get_books()
        filtered_books = [book for book in all_books if book.get_genre().lower() == genre.lower()]
        return filtered_books

    def search_by_genre_without_permutation(self, genre):
        results = self.filter_books_by_genre(genre)
        if not results:
            messagebox.showinfo("No Results", f"No books found for genre: {genre}")
            return
        self.display_results_in_tree(results)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GUI()
    app.run()
