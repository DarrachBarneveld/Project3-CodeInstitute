"""Module functions for displaying info to terminal with a clean UI"""

import os
import sys
import time
import colorama
from tabulate import tabulate


colorama.init()

G = colorama.Fore.LIGHTGREEN_EX
R = colorama.Fore.RED
B = colorama.Fore.CYAN
Y = colorama.Fore.YELLOW
W = colorama.Fore.WHITE
M = colorama.Fore.MAGENTA


def display_welcome():
    """
    Display ASCII welcome Log logo on the terminal.
    """
    print(G + ' _    _            _   _____ _   _____       _  ')
    print(G + '| |  | |          | | |_   _| | |  _  |     | |  ')
    print(G + '| |  | | ___  _ __| | __| | | |_| | | |_   _| |_ ')
    print(B + "| |/\| |/ _ \| '__| |/ /| | | __| | | | | | | __|")
    print(B + '\  /\  / (_) | |  |   <_| |_| |_\ \_/ / |_| | |_ ')
    print(B + ' \/  \/ \___/|_|  |_|\_\___/ \__|\___/ \__,_|\__|')
    print(' ')
    print(R + '                             By Darrach Barneveld')
    print(W)


def logout():
    """
    UI display of logging a user out
    """

    print(R)
    type_text('Logging out.....')
    time.sleep(1)

def type_text(string, speed=.03):
    """
    Displays a string in a typed out animation by printing text periodically
    
    Args:
        string (str): The string to print to the console
        speed (int): A number to configure speed of animation 
    """
    for character in string:
        time.sleep(speed)
        sys.stdout.write(character)
        sys.stdout.flush()

def display_text(text_array, speed):
    """
    Loops through an array of strings and prints them to the console in an animated manner
    
    Args:
        text_array (Arr[str]): An array of strings
        speed (int): A number to configure speed of animation 
    """
    for text in text_array:
        print(text[0])
        type_text(text[1], speed)
        time.sleep(.1)
    print(W + '\n')


def clear_screen():
    """
    Clears terminal screen for fresh UI for user.
    """

    os.system('cls' if os.name == 'nt' else "printf '\033c'")


def back_to_home():
    """
    Allows user to hit enter to go back to home.
    """
    print('\n')
    input("Press any key to continue...")
    clear_screen()


def display_error(string):
    """
    Displays an error message to the user.
    """
    print(R + string)
    print(W + '\n')


def format_macro_data(data):
    """
    Formats object data into a table. Prints the table to the terminal.
    
    Args:
        data (obj): An object containing strings and nested objects
    """
    clear_screen()

    print(G)
    type_text('Custom macro nutrient information', .03)
    table_data = []
    table_headers = [Y + "DIET"]

    for key, value in data.items():
        if isinstance(value, dict):
            for nested_key, _ in value.items():
                table_headers.append(nested_key.upper())
            # for nested_key, nested_value in value.items():
            table_data.append([W + key.capitalize() ,value['protein'], value['fat'], 
            value['carbs']])
    print(Y)
    table = tabulate(table_data, table_headers, tablefmt="fancy_grid")
    print(table)
    back_to_home()

def format_user_data(data):
    """
    Formats object data into a table. Prints the table to the terminal.
    
    Args:
        data (obj): An object containing strings and nested objects
    """

    table_headers = ["WEIGHT", 'HEIGHT', 'AGE', 'GENDER', 'ACTIVITY_LEVEL']
    table_data = [data[3], data[4], data[5], data[6].upper(), data[7]]
    clear_screen()
    print(G)
    type_text('Your Current Metrics', .03)

    print(W)
    table = tabulate([table_data], table_headers, tablefmt="fancy_grid")
    print(table)


def format_daily_calories(data):
    """
    Formats object data into a table. Prints the table to the terminal.
    
    Args:
        data (obj): An object containing strings and nested objects
    """
    clear_screen()

    print(G)
    type_text('Recommended caloric intake', .03)

    print(f"Basal Metabolic Rate = {data['BMR']}")
    table_data = []
    table_headers = [Y + "GOAL", 'WEEKLY CHANGE', 'CALORIES']
    for key, value in data['goals'].items():
        if isinstance(value, dict):
            table_data.append([W + key , list(value.values())[0], value['calory']])
    print(Y)
    table = tabulate(table_data, table_headers, tablefmt="fancy_grid")
    print(table)
    back_to_home()


def format_bmi(data):
    """
    Formats object data into a table. Prints the table to the terminal.
    
    Args:
        data (obj): An object containing key value pairs
    """

    clear_screen()
    print(G)
    type_text('Your BMI Results', .03)

    table_data = []

    table_headers = [Y + "BMI", 'HEALTH', 'HEALTH RANGE']
    for _, value in data.items():
        table_data.append(W + str(value))
    table = tabulate([table_data], table_headers, tablefmt="fancy_grid")
    print(Y)
    print(table)
    back_to_home()
