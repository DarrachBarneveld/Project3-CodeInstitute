import requests
from config import RAPID_API_HEADERS

url = "https://fitness-calculator.p.rapidapi.com/idealweight"


def request_fitness_calculator(url=url, params=None , data=None):
    """
    Sends a request to a Fitness Calculator API and returns the response.

    Parameters:
        url (str): The URL of the API endpoint.
        params (dict): Query parameters to be included in the request URL (default: None).
        data (dict): Data to be sent in the request body (default: None).

    Returns:
        requests.Response: The response object from the API.
    """


    try:
        response = requests.get(url, headers=RAPID_API_HEADERS, params=params, timeout=10)


        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as error:
        print(error)
        return None