import requests
from config import RAPID_API_HEADERS

def validate_strings(input_string, valid_strings):
    """
    Checks if the input string is valid by verifying if it is present in the list of valid strings.

    Parameters:
        input_string (str): The input string to check.
        valid_strings (list): A list of valid strings to compare against.

    Raises:
        ValueError: If the input string is not found in the list of valid strings.
    """
    try:
        if input_string.lower() in valid_strings:
            return True
        if input_string.lower() not in valid_strings:
            raise ValueError
    except ValueError:
        print("Invalid input string")
  


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
        print(f"Invalid integer. The number must be in the range of {min_value}-{max_value}.")

def bmi_calculator():
    """
    Sends a request to calculate BMI to a Fitness Calculator API and returns the response.

    Parameters:

    Returns:
        requests.Response: The response object from the API in json format.
    """

    valid_input_age = False
    valid_input_weight = False
    valid_input_height = False


    while not valid_input_age:
        age = input('What is your current age: ')
        if validate_number_in_range(number=age, min_value=10, max_value=100):
            valid_input_age = True

    while not valid_input_weight:
        weight = input('What is your current weight in kg: ')
        if validate_number_in_range(number=weight, min_value=40, max_value=160):
            valid_input_weight = True

    while not valid_input_height:
        height = input('What is your current height in cm: ')
        if validate_number_in_range(number=height, min_value=130, max_value=230):
            valid_input_height = True

    querystring = {"age": age, "weight": weight, "height": height}


    try:
        response = requests.get('https://fitness-calculator.p.rapidapi.com/bmi', headers=RAPID_API_HEADERS, params=querystring, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as error:
        print(error)
        return None
    

def daily_calories():
    """
    Sends a daily calories request to a Fitness Calculator API and returns the response.

    Returns:
        requests.Response: The response object from the API in json format.
    """

  
    valid_input_age = False
    valid_input_weight = False
    valid_input_height = False
    valid_activity_level = False
    valid_input_gender = False

    while not valid_input_age:
        age = input('What is your current age: ')
        if validate_number_in_range(number=age, min_value=10, max_value=100):
            valid_input_age = True

    while not valid_input_weight:
        weight = input('What is your current weight in kg: ')
        if validate_number_in_range(number=weight, min_value=40, max_value=160):
            valid_input_weight = True

    while not valid_input_height:
        height = input('What is your current height in cm: ')
        if validate_number_in_range(number=height, min_value=130, max_value=230):
            valid_input_height = True

    while not valid_activity_level:
        activty_level = input('What is your activty level from 1 - 6: ')
        if validate_number_in_range(number=activty_level, min_value=1, max_value=6):
            valid_activity_level = True

    while not valid_input_gender:
        gender = input('Male or Female: ')
        if validate_strings(input_string=gender, valid_strings=["female", "male"]):
            valid_input_gender = True

    activty_level = 'level_' + activty_level
    querystring = {"age":age,"gender":gender.lower(),"height":height,"weight":weight,"activitylevel":"level_1"}
    
    try:
        response = requests.get('https://fitness-calculator.p.rapidapi.com/dailycalorie', headers=RAPID_API_HEADERS, params=querystring, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as error:
        print(error)
        return None
