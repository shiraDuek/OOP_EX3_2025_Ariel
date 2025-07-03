import csv
from werkzeug.security import generate_password_hash, check_password_hash

import Inventory
import User


class UserManagement:
    """
    A class to manage user-related operations such as creating users,
    authenticating users, and maintaining a list of users.
    """
    FILE_NAME = "users.csv"

    def __init__(self):
        """
        Initialize the UserManagement instance and create the users file if it doesn't exist.
        """
        self.create_users_file()
        self.user_list = {}

    def create_users_file(self):
        """
        Create a CSV file to store user information if it doesn't already exist.
        """
        try:
            with open(self.FILE_NAME, mode="x", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["username", "password_hash", "active", "role"])  # Updated headers
        except FileExistsError:
            pass  # If the file exists, do nothing

    def user_exists(self, username):
        """
        Check if a username already exists in the system.

        :param username: The username to check for existence.
        :return: True if the username exists, False otherwise.
        """
        try:
            with open(self.FILE_NAME, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username:
                        return True
            return False
        except FileNotFoundError:
            return False

    def add_user(self, username, password, role="Librarian", active=1):
        """
        Add a new user with a hashed password.

        :param username: The username of the new user.
        :param password: The password of the new user.
        :param role: The role of the new user (default is 'Librarian').
        :param active: The active status of the new user (default is 1).
        """
        password_hash = generate_password_hash(password)
        with open(self.FILE_NAME, mode="a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([username, password_hash, active, role])  # Updated to include new columns
        self.update_users_dict()

    def authenticate_user(self, username, password):
        """
        Authenticate a user by checking the hashed password.

        :param username: The username of the user to authenticate.
        :param password: The password of the user to authenticate.
        :return: True if authentication is successful, False otherwise.
        """
        try:
            with open(self.FILE_NAME, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username:
                        return check_password_hash(row["password_hash"], password)
            return False
        except FileNotFoundError:
            return False

    def update_users_dict(self):
        """
        Update the user_list dictionary with all users from the file.
        """
        try:
            with open(self.FILE_NAME, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.user_list = {row["username"]: row["password_hash"] for row in reader}
        except FileNotFoundError:
            self.user_list = {}

    def get_user_from_csv(self, username):
        """
        Retrieve a user from the CSV file based on the username.

        :param username: The username of the user to retrieve.
        :return: A User instance if the user is found, None otherwise.
        """
        try:
            with open(self.FILE_NAME, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username:
                        password = row["password_hash"]
                        role = row["role"]
                        return UserFactory.create_user(username, password, role)
            return None
        except FileNotFoundError:
            return None

class UserFactory:
    """
    A factory class to create User instances based on the role.
    """

    @staticmethod
    def create_user(username, password, role="Librarian"):
        """
        Create a User instance based on the role.

        :param username: The username of the user.
        :param password: The password of the user.
        :param role: The role of the user (default is 'Librarian').
        :return: A User instance corresponding to the role.
        """
        switcher = {
            "Librarian": User.Librarian(username, password, Inventory.Inventory()),
        }
        return switcher.get(role, None)