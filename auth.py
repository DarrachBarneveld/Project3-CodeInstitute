"""This module provides functions for user authentication and authorization"""
import re
import colorama
import ui
from fitness_calculator import validate_strings, validate_input

colorama.init()


G = colorama.Fore.LIGHTGREEN_EX
R = colorama.Fore.LIGHTGREEN_EX
W = colorama.Fore.WHITE


def login(dataframe):
    """
    Login function that verifies the email and password in a Pandas DataFrame.

    Args:
        dataframe (DataFrame): The DataFrame containing user data.

    Returns:
        str or None: The email address if the login is successful,
        or None if the login fails.

    """
    print('\n')
    email = input("Enter your email: ").lower()
    password = input("Enter your password: ")

    database_password = dataframe['Password'].str.lower()
    database_email = dataframe['Email'].str.lower()

    matched_users = dataframe[
        (database_password == password) &
        (database_email == email)]

    # Authenticate the user based on the match
    if len(matched_users) > 0:
        first_name = matched_users['Firstname'].values[0]
        ui.clear_screen()
        print(
            "Authentication successful! "
            f"Welcome back {G + first_name.capitalize()}\n"
            )
        return email

    ui.display_error("Authentication failed. Please Try again.")
    return None


def signup(spreadsheet):
    """
    Signup function that appends a user's data as a row to a Google Sheet.

    Args:
        spreadsheet (object): The Google Sheet to append the row.

    Returns:
        str: A current user email.

    Raises:
        Exception: For any other unknown errors that may occur
        during the signup process.
    """
    print('\n')

    user_sheet = spreadsheet.get_worksheet(0)

    first_name = input("Enter your first name: ")
    while not is_alphabetic(first_name):
        first_name = input("Enter your first name: ")

    last_name = input("Enter your last name: ")
    while not is_alphabetic(last_name):
        last_name = input("Enter your last name: ")

    email = input("Enter your email: ")
    while not is_valid_email(email):
        email = input("Enter your email: ")

    password = input("Enter your password: ")
    while not is_valid_password(password):
        password = input("Enter your password: ")

    all_users = user_sheet.get_all_values()
    filtered_data = [row for row in all_users if row[2] == email]

    while len(filtered_data) > 0:
        ui.display_error('Email already in use')
        email = input("Enter your email: ")
        filtered_data = [row for row in all_users if row[2] == email]

    age, weight, height, gender, activty_level = define_base_inputs()
    user_data = [
        first_name, last_name,
        email, weight, height, age,
        gender, activty_level, password
        ]

    try:
        user_sheet.append_row(user_data)
        ui.clear_screen()

        print(f"Sign-up successful Welcome {G + first_name}\n")
        return email

    # pylint: disable=pylint(broad-exception-caught)
    except Exception as exc:
        # pylint: disable=pylint(broad-exception-raised)
        raise Exception("There was an error signing up!") from exc


def define_base_inputs():
    """
    Defines and validates the base input ranges for API requests

    Returns:
        Returns validated value inputs for age, weight, height, level,
        gender in an array
    """

    ui.clear_screen()

    print(G)
    ui.type_text(
        "Before we begin we need some information from you :)",
        speed=.01)
    print(W)

    age = validate_input('What is your current age? ', 10, 100)
    weight = validate_input(
        'What is your current weight in kg? ',
        40, 160)
    height = validate_input('What is your current height in cm? ', 130, 230)
    activty_level = validate_input(
        'What is your activty level from 1 - 6? ',
        1, 6)
    gender = validate_strings(
        input_string='Male or Female: ',
        valid=["female", "male"]
        )

    return [age, weight, height, gender.lower(), activty_level]


def is_valid_email(email):
    """
    Check if the given email address is valid.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """

    if re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return True
    ui.display_error("Please enter a valid email address")
    return False


def is_valid_password(password):
    """
    Check if the given password is valid.

    Args:
        password (str): The password to be validated.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    if len(password) >= 6:
        return True
    ui.display_error(
        "Not a valid password. Password must be at least 6 characters long"
        )
    return False


def is_alphabetic(string):
    """
    Check if the given input string contains only alphabetic letters.

    Args:
        string (str): The input string to be validated.

    Returns:
        bool: True if the input contains only alphabetic letters,
        False otherwise.
    """
    if string.isalpha():
        return True
    ui.display_error("Not a valid name. Must only contain alphabetic letters")
    return False


def authenticate_user(dataframe, spreadsheet):
    """
    Prompt the user for a choice of 'login' or 'signup'.

    Args:
        dataframe (object): The google user workout as a pandas dataframe.
        sheet (float): The google user worksheet.

    Returns:
        str: The the current user as an email.
    """

    choice = ''

    while choice not in ["login", "signup"]:
        choice = input("Choose 'login' or 'signup': ").lower()
        if choice not in ["login", "signup"]:
            ui.display_error(
                "Invalid choice. Please enter 'login' or 'signup'."
                )
    if choice == 'login':
        return login(dataframe)
    if choice == 'signup':
        return signup(spreadsheet)
    return None
