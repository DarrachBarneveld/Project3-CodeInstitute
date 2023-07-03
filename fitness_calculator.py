import requests
from config import RAPID_API_HEADERS


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

def bmi_calculator(url):
    """
    Sends a request to a Fitness Calculator API and returns the response.

    Parameters:
        url (str): The URL of the API endpoint.
        params (dict): Query parameters to be included in the request URL (default: None).
        data (dict): Data to be sent in the request body (default: None).

    Returns:
        requests.Response: The response object from the API.
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
        response = requests.get(url, headers=RAPID_API_HEADERS, params=querystring, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as error:
        print(error)
        return None