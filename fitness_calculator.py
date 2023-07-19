"""This module provides functions API fitness calculator calculations """
import os
from dotenv import load_dotenv
import colorama
import requests
import ui

colorama.init()

R = colorama.Fore.RED
W = colorama.Fore.WHITE
G = colorama.Fore.LIGHTGREEN_EX

load_dotenv()

# Retriving the API secret keys from config file
RAPID_API_HEADERS = {
 	"X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
 	"X-RapidAPI-Host": os.getenv('RAPID_API_HOST')
     }

# pylint: disable=line-too-long
WEIGHT_GOAL_OPTIONS =  [['Maintain weight', 'maintain'], ['Mild Weight Loss', 'mildlose'], ['Weight Loss', 'weightlose'], ['Extreme Weight Loss', 'extremelose'], ['Mild Weight Gain', 'mildgain'], ["Weight Gain", 'weightgain'], ["Extreme Weight Gain", 'extremegain']]


def validate_strings(input_string, valid_strings):
    """
    Checks if the input string is valid by verifying if it is present in the list of valid strings.

    Parameters:
        input_string (str): The input string for the question
        valid_strings (list): A list of valid strings to compare against.

    Raises:
        Returns the validated choice
    """

    choice = ''

    while choice not in valid_strings:
        choice = input(input_string).lower()
        if choice not in valid_strings:
            ui.display_error(f"Invalid choice. Please enter {valid_strings[0]} or {valid_strings[1]}.")

    return choice


def validate_number_in_range(number, min_value, max_value):
    """
    Checks if the input value is a number and within the specified range.

    Parameters:
        input_value (str or int or float): The input value to check.
        min_value (int or float): The minimum allowed value.
        max_value (int or float): The maximum allowed value.

    Returns:
        bool: True if the input value is a number and within the specified range, False otherwise.
    """
    try:
        input_value = int(number)
        if input_value < min_value or input_value > max_value:
            raise ValueError
        if min_value <= input_value <= max_value:
            return True
    except ValueError:
        ui.display_error(f"Invalid integer. The number must be in the range of {min_value}-{max_value}.")
    return False


def bmi_calculator(user_data):
    """
    Sends a request to calculate BMI to a Fitness Calculator API and returns the response.


    Returns:
        requests.Response: The response object from the API in json format.
    """

    weight, height, age, _, _ = define_user_data(user_data)

    querystring = {"age": age, "weight": weight, "height": height}


    try:
        response = requests.get('https://fitness-calculator.p.rapidapi.com/bmi', headers=RAPID_API_HEADERS, params=querystring, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json().get('data')
    except requests.exceptions.RequestException as error:
        print(error)
        return None

def validate_input(string, mini, maxi):
    """
    Validates the age of a user

    Parameters:
        string (str): The input string to display to user.
        mini (int): The minimum allowed value.
        maxi (int): The maximum allowed value.

    Returns:
    The validated input
    """

    valid_input = False

    while not valid_input:
        metric = input(string)
        if validate_number_in_range(number=metric, min_value=mini, max_value=maxi):
            valid_input = True

    return metric


def daily_calories(user_data):
    """
    Sends a daily calories request to a Fitness Calculator API and returns the response.

    Returns:
        requests.Response: The response object from the API in json format.
    """
    weight, height, age, gender, activty_level = define_user_data(user_data)
    activty_level = 'level_' + activty_level

    querystring = {"age":age,"gender":gender.lower(),"height":height,"weight":weight,"activitylevel":activty_level}

    try:
        response = requests.get('https://fitness-calculator.p.rapidapi.com/dailycalorie', headers=RAPID_API_HEADERS, params=querystring, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json().get('data')
    except requests.exceptions.RequestException as error:
        print(error)
        return None


def define_user_data(user_data):
    """
    Receives an array of user data and formats required data it for easy destructuring

    Returns:
        An array of necessary and malleable user data
    """
    weight = user_data[3]
    height = user_data[4]
    age = user_data[5]
    gender = user_data[6]
    activity_level = user_data[7]

    return [weight, height, age, gender, activity_level]



def dieting_macros(user_data):
    """
    Sends a dieting macros request to a Fitness Calculator API and returns the response.

    Returns:
        requests.Response: The response object from the API in json format.
    """
    valid_input_goal = False

    weight, height, age, gender, activty_level = define_user_data(user_data)

    goal = ''

    while not valid_input_goal:
        print(G)
        for i, option in enumerate(WEIGHT_GOAL_OPTIONS):
            ui.type_text(f"{i+1}. {option[0]} \n", .01)
        print(W)
        choice = input("What are your goals? Enter the corrosponding number: ")

        try:
            index = int(choice) - 1
            if 0 <= index < len(WEIGHT_GOAL_OPTIONS):
                goal = WEIGHT_GOAL_OPTIONS[index][1]
                valid_input_goal = True
            else:
                ui.display_error("Invalid choice. Please enter a valid number ")
        except ValueError:
            ui.display_error("Invalid choice. Please enter a valid number.")

    querystring = {"age":age, "gender":gender.lower(),"height":height,"weight":weight,"activitylevel":activty_level, "goal":goal}

    try:
        response = requests.get('https://fitness-calculator.p.rapidapi.com/macrocalculator', headers=RAPID_API_HEADERS, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json().get('data')
    except requests.exceptions.RequestException as error:
        ui.display_error(str(error))
        return None
