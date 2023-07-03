from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from auth import login, signup
from config import GOOGLE_SHEETS_SCOPE
from fitness_calculator import request_fitness_calculator


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(GOOGLE_SHEETS_SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SPREADSHEET = GSPREAD_CLIENT.open('WorkItOut')

USERS_SHEET = SPREADSHEET.get_worksheet(0)
WORKOUT_SHEET = SPREADSHEET.get_worksheet(1)

EXERCISES = ['running', 'swimming', 'cycling', 'weights', 'sports']

sheet_data = USERS_SHEET.get_all_values()
df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

CURRENT_USER = ''


def select_options():
    """
    Displays a list of options and prompts the user to select one.

    Returns:
        str: The selected option.
    """
    options = ['Enter Workout', 'View Workouts', 'Check BMI', 'Recommended Macros', 'Recommended Daily Calories']
    
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    

    while True:
        choice = input("Enter the number corresponding to your choice: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(options):
                if index == 0:
                    create_new_workout()
                elif index == 1:
                    view_all_workouts()
                elif index == 2:
                    request_fitness_calculator()
                elif index == 3:
                    request_fitness_calculator()
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a valid number.")

    
    

def view_all_workouts():
    return True

def create_new_workout():
    workout_type = input('What workout type did you do?')
    workout_duration = input('For how long did you workout in whole minutes?')
    validate_data(workout_type, workout_duration)

    update_workout_sheet(workout_type, workout_duration)


def validate_data(type, duration):
    """
    Check if a inputed string is a valid exercise. Check if the duration is a number
    
    Args:
        string (str): The string to search for.
        EXERCISES (list): The array (list) to search in.
    
    Raises:
        ValueError: If the search string is not found in the array.
    """
    try:
        if type not in EXERCISES:
            raise ValueError(f"{type} does not exist in the array")
        else:
            print(type, "exists in the array")
        duration = int(duration)
        if 0 <= duration <= 240:
            return True  # Valid integer within the specified range
        else:
            raise ValueError(f"{duration} is not a number")
    except ValueError as error:
        print("Error:", str(error))
     
    return True

def update_workout_sheet(type, duration):
    """
    Update the Google Sheets Document if valid data
    
    Args:
        The current data within the Google Sheets Document
    
    Raises:
        ValueError: If the search string is not found in the array.
    """
    current_time = datetime.now().time()
    time_string = current_time.strftime("%H:%M:%S")

    workout_row = [CURRENT_USER, type, time_string, duration]
    WORKOUT_SHEET.append_row(workout_row)


def main():
    """
    Main Function to run code
    """
    select_options()


    # choice = input("Choose 'login' or 'signup': ").lower()
    # global CURRENT_USER

    # if choice == 'login':
    #    CURRENT_USER = login(df)
    # elif choice == 'signup':
    #     CURRENT_USER = signup(USERS_SHEET)
    # else:
    #     print("Invalid choice")

    
    # if CURRENT_USER:
    #     fitness_calculator()
    #     create_new_workout()


main()
