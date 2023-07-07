"""Module provides calles for manipulating dates and times"""
from datetime import datetime
import sys
import time
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound
import pandas as pd
import colorama
import fitness_calculator
from auth import authenticate_user

colorama.init()

G = colorama.Fore.GREEN
R = colorama.Fore.RED
B = colorama.Fore.CYAN
Y = colorama.Fore.YELLOW
W = colorama.Fore.WHITE
M = colorama.Fore.MAGENTA

GOOGLE_SHEETS_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

USERS_SHEET = None
WORKOUT_SHEET = None
DF = None



def load_google_sheets():
    """
    Load Google Sheets using the gspread library.

    Returns:
        spreedsheet: The google WorkItOut spreadsheet.

    Raises:
        gspread.exceptions.APIError: If an error occurs while accessing the Google Sheets API.
        gspread.exceptions.SpreadsheetNotFound: If the specified spreadsheet is not found.
        gspread.exceptions.WorksheetNotFound: If the default worksheet is not found.
        Exception if generalised error
    """
    try:
        # pylint: disable=pylint(global-statement)
        global USERS_SHEET
        global WORKOUT_SHEET
        global DF

        creds = Credentials.from_service_account_file('creds.json')
        scoped_creds = creds.with_scopes(GOOGLE_SHEETS_SCOPE)
        gspread_client = gspread.authorize(scoped_creds)

        spreadsheet = gspread_client.open('WorkItOut')
        USERS_SHEET = spreadsheet.get_worksheet(0)
        WORKOUT_SHEET = spreadsheet.get_worksheet(1)
        sheet_data = USERS_SHEET.get_all_values()
        DF = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

        print("Data accessed successfully.")
        return spreadsheet
    
    

    except APIError as exc:
        raise APIError('An API error occurred. Try again later!') from exc

    except SpreadsheetNotFound as exc:
        raise SpreadsheetNotFound("The spreadsheet was not found Try again later!") from exc

    except WorksheetNotFound as exc:
        raise WorksheetNotFound("The worksheet was not found. Try again later!") from exc
    
    except Exception as exc:
        raise Exception("The worksheet was not found. Try again later!") from exc
      
    



# pylint: disable=line-too-long
EXERCISES = [[Y, 'Running'], [Y,'Swimming'], [Y,'Cycling'], [Y, 'Weights'], [Y, 'Sports'], [Y ,"Light"]]
# pylint: disable=line-too-long
CHOICE_OPTIONS = [[R, '1. Enter Workout'], [G, '2. View Workouts'], [B, '3. Check BMI'], [Y, '4. Dieting Macros Calculator'], [M,'5. Recommended Daily Calories']]

INTRO_TEXT = [[W, 'Welcome to WorkItOut!\n'], [W, 'Track your workouts!\n'], [W,'Achieve your weight goals!\n'], [W, 'Access recommended nutritional information!\n']]





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


def select_options(current_user):
    """
    Displays a list of options and prompts the user to select one. Selected prompt will run an assosicated function

    Parameters:
        current_user(str): The authenticated user email

    Raises:
        ValueError: If the choice is invalid or not within the choice amount.
    """
    while True:
        display_text(CHOICE_OPTIONS, .01)
        choice = input("Enter the number corresponding to your choice: ")

        try:
            index = int(choice) - 1
            if 0 <= index < len(CHOICE_OPTIONS):
                if index == 0:
                    create_new_workout(current_user)
                elif index == 1:
                    view_all_workouts(current_user)
                elif index == 2:
                    data = fitness_calculator.bmi_calculator()
                    for key, value in data.items():
                        print(R + key.upper() + Y, "->", value) 
                elif index == 3:
                      data = fitness_calculator.dieting_macros()
                      format_macro_data(data)
                elif index == 4:
                    data = fitness_calculator.daily_calories()
                    print(data)
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

    try:
        all_workouts = WORKOUT_SHEET.get_all_values()

        filtered_data = [row for row in all_workouts if row[0] == current_user]

        for row in filtered_data:
            workout_type, workout_time, workout_duration = row[1:4]
            print("Type:", workout_type, "Time:", workout_time, "Duration:", workout_duration )
            print()  # Print an empty line between rows

    # pylint: disable=pylint(broad-exception-caught)
    except Exception as error:
        print("An error occurred:", str(error))


def create_new_workout(current_user):
    """
    Create a new workout in google sheets document with user inputs and authenticated user so workouts are saved with user data
    
    Args:
        current_user(str): The authenticated user email
    """

    workout_type = ''
    workout_duration = ''

    while workout_type == '':
        display_text(EXERCISES, .01)
        choice = input('What workout type did you do?')
        try:
            index = int(choice) - 1
            if 0 <= int(choice) < len(EXERCISES):
                workout_type = EXERCISES[index][1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a valid number.")

    while not isinstance(workout_duration, int):
        input_duration = input('For how long did you workout in whole minutes?')
        workout_duration = validate_duration(input_duration)


    update_workout_sheet(current_user,workout_type, workout_duration)


def validate_duration(duration):
    """
    Check if a inputed string is a valid exercise. Check if the duration is a number

    Args:
        duration (str): The amount of time a user worked out for

    Raises:
        ValueError: Raises the error that a number is not between 1 - 240
        ValueError: If the duration is not a number.
    """
    try:
        if 0 <= int(duration) <= 240:
            return int(duration)
        print('Duration must be between 1 and 240')
    except ValueError:
        print(f"{duration} is not a number")


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
    try:
        WORKOUT_SHEET.append_row(workout_row)
        print(Y + "Workout Added!")
        print(W)

    # pylint: disable=pylint(broad-exception-caught)
    except Exception as error:
        print("An error occurred:", str(error))





def display_text(text_array, speed):
    """
    Loops through an array of strings and prints them to the console in an animated manner
    
    Args:
        text_array (Arr[str]): An array of strings
        speed (int): A number to configure speed of animation 
    """
    print('\n')
    for text in text_array:
        print(text[0])
        type_text(text[1], speed)
        time.sleep(.1)
    print(W + '\n')


sample_data = {'BMR': 1192.5, 'goals': {'maintain weight': 2057.0625, 'Mild weight loss': {'loss weight': '0.25 kg', 'calory': 1807.0625}, 'Weight loss': {'loss weight': '0.50 kg', 'calory': 1557.0625}, 'Extreme weight loss': {'loss weight': '1 kg', 'calory': 1057.0625}, 'Mild weight gain': {'gain weight': '0.25 kg', 'calory': 2307.0625}, 'Weight gain': {'gain weight': '0.50 kg', 'calory': 2557.0625}, 'Extreme weight gain': {'gain weight': '1 kg', 'calory': 3057.0625}}}


def format_macro_data(data):
     for key, value in data.items():
        if isinstance(value, dict):
            result = " ".join([f"{n_key.upper()}: " f"{n_value}" for n_key, n_value in value.items()])
            result = result.split(" ")
            modified_array = [[result[i], B if i % 2 == 0 else Y] for i in range(len(result))]
            for index, subarray in enumerate(modified_array):
                if index % 6 == 0:
                    print()
                if index == 0:
                    print(R + f"{key.upper()}" + Y, "->", subarray[1] + subarray[0], end=" ")
                else:
                    print(subarray[1] + subarray[0], end=" ")
                                    
        else:
            print(R + key.upper() + Y, "->", value)


def main():
    """
    Main Function to run code
    """

    display_welcome()
    display_text(INTRO_TEXT, .03)
    try:
        load_google_sheets()
    except Exception as error:
        print(error)
        return

    current_user = None
    while current_user is None:
        try:
            current_user = authenticate_user(DF, USERS_SHEET)
        except Exception as error:
            print(error)
    
    select_options(current_user)


main()
