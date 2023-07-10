"""Module provides calles for manipulating dates and times"""
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound
import pandas as pd
import colorama
from tabulate import tabulate
import fitness_calculator
from auth import authenticate_user
import ui


colorama.init()

G = colorama.Fore.LIGHTGREEN_EX
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
        return spreadsheet
    
    
    except APIError as exc:
        raise APIError('An API error occurred. Try again later!') from exc

    except SpreadsheetNotFound as exc:
        raise SpreadsheetNotFound("The spreadsheet was not found Try again later!") from exc

    except WorksheetNotFound as exc:
        raise WorksheetNotFound("The worksheet was not found. Try again later!") from exc
    
    # except Exception as exc:
    #     raise Exception("The worksheet was not found. Try again later!") from exc
    
# pylint: disable=line-too-long
EXERCISES = [[Y, '1. Running'], [Y,'2. Swimming'], [Y,'3. Cycling'], [Y, '4. Weights'], [Y, '5. Sports'], [Y ,"6. Light"], [Y ,"7. Other"]]
# pylint: disable=line-too-long
CHOICE_OPTIONS = [[G, '1. Enter Workout'], [G, '2. View Workouts'], [G, '3. Check BMI'], [G, '4. Dieting Macros Calculator'], [G,'5. Recommended Daily Calories']]
# pylint: disable=line-too-long
INTRO_TEXT = [[W, 'Welcome to WorkItOut!\n'], [W, 'Track your workouts!\n'], [W,'Achieve your weight goals!\n'], [W, 'Access recommended nutritional information!\n']]



def select_options(current_user):
    """
    Displays a list of options and prompts the user to select one. Selected prompt will run an assosicated function

    Parameters:
        current_user(str): The authenticated user email

    Raises:
        ValueError: If the choice is invalid or not within the choice amount.
    """
    while True:
        print(W + 'What would you like to do?')
        ui.display_text(CHOICE_OPTIONS, .01)
        choice = input("Enter the number corresponding to your choice: ")

        try:
            index = int(choice) - 1
            if 0 <= index < len(CHOICE_OPTIONS):
                if index == 0:
                    create_new_workout(current_user)
                elif index == 1:
                    view_all_workouts(current_user)
                    print('\n')
                    ui.back_to_home()
                elif index == 2:
                    data = fitness_calculator.bmi_calculator()
                    ui.format_bmi(data)
                elif index == 3:
                    data = fitness_calculator.dieting_macros()
                    ui.format_macro_data(data)
                elif index == 4:
                    data = fitness_calculator.daily_calories()
                    ui.format_daily_calories(data)
            else:
                print(R + "\nInvalid choice. Please enter a valid number.\n" + W )
        except ValueError:
            print(R + "\nInvalid choice. Please enter a valid number.\n" + W )


def view_all_workouts(current_user):
    """
    Retrieves data from a Google Sheets spreadsheet.

    Parameters:
        current_user(str): The authenticated user email
    """

    try:
        ui.clear_screen()
        print(Y + 'Here are you workouts')
        all_workouts = WORKOUT_SHEET.get_all_values()

        filtered_data = [row for row in all_workouts if row[0] == current_user]
        table_data = []
        table_headers = ["WORKOUT", 'DATE', 'DURATION']

        for row in filtered_data:
            workout_type, workout_date, workout_duration = row[1:4]
            table_data.append([W + str(workout_type), W + str(workout_date), W + str(workout_duration)])
        
        table = tabulate(table_data, table_headers, tablefmt="fancy_grid")
        print(Y)
        print(table)
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
    ui.clear_screen()


    while workout_type == '':
        ui.display_text(EXERCISES, .01)
        print('What type of workout did you do? \n')
        choice = input('Enter the number corresponding to your choice: ')
        print('\n')
        try:
            index = int(choice) - 1
            if 0 <= int(choice) < len(EXERCISES):
                workout_type = EXERCISES[index][1]
            else:
                print(R + "\nInvalid choice. Please enter a valid number.\n" + W )
        except ValueError:
            print(R + "\nInvalid choice. Please enter a valid number.\n" + W )

    while not isinstance(workout_duration, int):
        input_duration = input('For how long did you workout in whole minutes? ')
        print('\n')

        workout_duration = validate_duration(input_duration)
        workout_type = workout_type.split('. ')[1]


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

    current_date = datetime.now().date()
    date_string = current_date.strftime("%Y-%m-%d")



    workout_row = [current_user, workout_type, date_string, duration]
    try:
        WORKOUT_SHEET.append_row(workout_row)
        ui.clear_screen()
        print(Y + "Workout Added!")
        print(W)

    # pylint: disable=pylint(broad-exception-caught)
    except Exception as error:
        print("An error occurred:", str(error))



def main():
    """
    Main Function to run code
    """

    # display_welcome()
    # display_text(INTRO_TEXT, .03)

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
