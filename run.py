"""Module provides calles for manipulating dates and times"""
from datetime import datetime
import sys
import time
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import colorama
import fitness_calculator
from auth import login, signup

colorama.init()

G = colorama.Fore.GREEN
R = colorama.Fore.RED
B = colorama.Fore.CYAN
Y = colorama.Fore.YELLOW
W = colorama.Fore.WHITE



GOOGLE_SHEETS_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(GOOGLE_SHEETS_SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SPREADSHEET = GSPREAD_CLIENT.open('WorkItOut')

USERS_SHEET = SPREADSHEET.get_worksheet(0)
WORKOUT_SHEET = SPREADSHEET.get_worksheet(1)

EXERCISES = ['running', 'swimming', 'cycling', 'weights', 'sports']
# pylint: disable=line-too-long
CHOICE_OPTIONS = ['Enter Workout', 'View Workouts', 'Check BMI', 'Dieting Macros Calculator', 'Recommended Daily Calories']

INTRO_TEXT = ['Welcome to WorkItOut!\n', 'Track your workouts!\n', 'Achieve your weight goals!\n', 'Access recommended nutritional information!\n']

sheet_data = USERS_SHEET.get_all_values()
df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])



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



# Credit author of animation
def type_text(string):
    """
    Displays a string in a typed out animation by printing text periodically
    """
    for character in string:
        time.sleep(.03)
        sys.stdout.write(character)
        sys.stdout.flush()


def select_options(current_user):
    """
    Displays a list of options and prompts the user to select one. Selected prompt will run an assosicated function

    Parameters:
        current_user(str): The authenticated user email

    Raises:
        ValueError: If the choice is invalid or not within the choice amount.
    """
    while True:
        for i, option in enumerate(CHOICE_OPTIONS):
            print(f"{i+1}. {option}")
        choice = input("Enter the number corresponding to your choice: ")

        try:
            index = int(choice) - 1
            if 0 <= index < len(CHOICE_OPTIONS):
                if index == 0:
                    create_new_workout(current_user)
                elif index == 1:
                    view_all_workouts(current_user)
                elif index == 2:
                    response = fitness_calculator.bmi_calculator()
                    print(response)
                elif index == 3:
                    response = fitness_calculator.dieting_macros()
                    print(response)
                elif index == 4:
                    response = fitness_calculator.daily_calories()
                    print(response)
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a valid number.")


def view_all_workouts(current_user):
    """
    Retrieves data from a Google Sheets spreadsheet.

    Parameters:
        current_user(str): The authenticated user email
    """
    all_workouts = WORKOUT_SHEET.get_all_values()

    filtered_data = [row for row in all_workouts if row[0] == current_user]

    for row in filtered_data:
        workout_type, workout_time, workout_duration = row[1:4]
        print("Type:", workout_type, "Time:", workout_time, "Duration:", workout_duration )
        print()  # Print an empty line between rows


def create_new_workout(current_user):
    """
    Create a new workout in google sheets document with user inputs and authenticated user so workouts are saved with user data
    
    Args:
        current_user(str): The authenticated user email
    """
    workout_type = input('What workout type did you do?')
    workout_duration = input('For how long did you workout in whole minutes?')
    validate_data(workout_type, workout_duration)

    update_workout_sheet(current_user,workout_type, workout_duration)


def validate_data(workout_type, duration):
    """
    Check if a inputed string is a valid exercise. Check if the duration is a number
    
    Args:
        workout_type (str): The type of workout to search for.
        duration (str): The amount of time a user worked out for
    
    Raises:
        ValueError: If the search string is not found in the array.
        ValueError: If the duration is not a number.
    """
    try:
        if workout_type not in EXERCISES:
            raise ValueError(f"{workout_type} does not exist in the array")
        duration = int(duration)
        if not 0 <= duration <= 240:
            raise ValueError(f"{duration} is not a number")
             
    except ValueError as error:
        print("Error:", str(error))
    return True


def update_workout_sheet(current_user, workout_type, duration):
    """
    Update the Google Sheets Document if valid data
    
    Args:
        current_user (str): The authenticated user email
        type (str): The type of workout
        duration (str): The duration of the workout
    """
    current_time = datetime.now().time()
    time_string = current_time.strftime("%H:%M:%S")

    workout_row = [current_user, workout_type, time_string, duration]
    WORKOUT_SHEET.append_row(workout_row)



def display_text(textArray):
    for text in textArray:
        type_text(text)
        time.sleep(.5)
        print('\n')


def main():
    """
    Main Function to run code
    """

    display_welcome()
    display_text(INTRO_TEXT)
 


    choice = input("Choose 'login' or 'signup': ").lower()
    current_user = ''

    if choice == 'login':
        current_user = login(df)
    elif choice == 'signup':
        current_user = signup(USERS_SHEET)
    else:
        print("Invalid choice")
    if current_user:
        select_options(current_user)
    else:
        print('No current user')


main()
