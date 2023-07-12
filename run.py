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

# pylint: disable=line-too-long
EXERCISES = [[Y, '1. Running'], [Y,'2. Swimming'], [Y,'3. Cycling'], [Y, '4. Weights'], [Y, '5. Sports'], [Y ,"6. Light"], [Y ,"7. Other"]]
# pylint: disable=line-too-long
CHOICE_OPTIONS = [[G, '1. Enter Workout'], [G, '2. View Workouts'], [G, '3. Check BMI'], [G, '4. Dieting Macros Calculator'], [G,'5. Recommended Daily Calories'], [B,'6. Edit Body Metrics']]
# pylint: disable=line-too-long
INTRO_TEXT = [[W, 'Welcome to WorkItOut!\n'], [W, 'Track your workouts!\n'], [W,'Achieve your weight goals!\n'], [W, 'Access recommended nutritional information!\n']]


def load_google_sheets():
    """
    Load Google Sheets using the gspread library.

    Returns:
        array: Google usersheet, workoutsheet and the pandas user Dataframe.

    Raises:
        gspread.exceptions.APIError: If an error occurs while accessing the Google Sheets API.
        gspread.exceptions.SpreadsheetNotFound: If the specified spreadsheet is not found.
        gspread.exceptions.WorksheetNotFound: If the default worksheet is not found.
        Exception if generalised error
    """
    try:

        creds = Credentials.from_service_account_file('creds.json')
        scoped_creds = creds.with_scopes(GOOGLE_SHEETS_SCOPE)
        gspread_client = gspread.authorize(scoped_creds)

        spreadsheet = gspread_client.open('WorkItOut')
        user_sheet = spreadsheet.get_worksheet(0)
        user_sheet_data = user_sheet.get_all_values()
        dateframe = pd.DataFrame(user_sheet_data[1:], columns=user_sheet_data[0])
        return [spreadsheet, dateframe]

    except APIError as exc:
        raise APIError('An API error occurred. Try again later!') from exc

    except SpreadsheetNotFound as exc:
        raise SpreadsheetNotFound("The spreadsheet was not found Try again later!") from exc

    except WorksheetNotFound as exc:
        raise WorksheetNotFound("The worksheet was not found. Try again later!") from exc

    except Exception as exc:
        raise Exception("The worksheet was not found. Try again later!") from exc


def select_options(current_user, spreadsheet):
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
        ui.clear_screen()

        try:
            index = int(choice) - 1
            if 0 <= index < len(CHOICE_OPTIONS):
                if index == 0:
                    create_new_workout(current_user, spreadsheet.get_worksheet(1))
                elif index == 1:
                    view_all_workouts(current_user, spreadsheet.get_worksheet(1))
                    print('\n')
                    ui.back_to_home()
                elif index == 2:
                    data = fitness_calculator.bmi_calculator()
                    ui.format_bmi(data)
                elif index == 3:

                    user_data = get_current_user_data(current_user, spreadsheet.get_worksheet(0))
                    ui.format_user_data(user_data)
                    data = fitness_calculator.dieting_macros()
                    ui.format_macro_data(data)
                elif index == 4:
                    data = fitness_calculator.daily_calories()
                    ui.format_daily_calories(data)
                elif index == 5:
                    display_current_metrics(current_user, spreadsheet.get_worksheet(0))
            else:
                print(R + "\nInvalid choice. Please enter a valid number.\n" + W )
        except ValueError:
            print(R + "\nInvalid choice. Please enter a valid number.\n" + W )


def view_all_workouts(current_user, workout_sheet):
    """
    Retrieves data from a Google Sheets spreadsheet.

    Parameters:
        current_user(str): The authenticated user email
    """

    try:
        ui.clear_screen()
        print(Y + 'Here are you workouts')
        all_workouts = workout_sheet.get_all_values()

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



def create_new_workout(current_user, workout_sheet):
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


    update_workout_sheet(current_user,workout_type, workout_duration, workout_sheet)


def get_current_user_data(current_user, user_sheet): 
    all_users = user_sheet.get_all_values()
    user_data = [row for row in all_users if row[0] == current_user]
    return user_data[0]


def display_current_metrics(current_user, user_sheet):
    editable_data = ['Weight', 'Height', 'Age', "Gender", "Activty Level", "Go Back"]

    user_data = get_current_user_data(current_user, user_sheet)

    ui.format_user_data(user_data)

    for i, option in enumerate(editable_data):
        print(B + f"{i+1}. {option}")
    print(W)

    edit_choice = ''

    while edit_choice == '':
        choice = input("What do you wish to edit? ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(editable_data):
                edit_choice = editable_data[index]
                # update_user_metrics(current_user, user_sheet)
            else:
                ui.display_error("Invalid choice. Please enter a valid number ")
        except ValueError:
            ui.display_error("Invalid choice. Please enter a valid number.")


    update_user_metrics(edit_choice, user_data[0], user_sheet)



def update_user_metrics(metric, user_data, user_sheet):

    new_value = ''

    if metric == 'Age':
        new_value = fitness_calculator.validate_input('What is your current age? ', 10, 100)
    elif metric == 'Weight':
        new_value = fitness_calculator.validate_input('What is your current weight in kg? ', 40, 160)
    elif metric == 'Height':
        new_value = fitness_calculator.validate_input('What is your current height in cm? ', 130, 230)
    elif metric == 'Activty Level':
        new_value = fitness_calculator.validate_input('What is your activty level from 1 - 6? ', 1, 6)
    elif metric == 'Gender':
        new_value = fitness_calculator.validate_gender()

    else:
        ui.clear_screen()
        return

    all_values = user_sheet.get_all_values()
    header_row = all_values[0]
    email_column_index = header_row.index("Email")
    metric_column_index = header_row.index(metric) + 1


    row_index = None
    for i, row in enumerate(all_values):
        if row[email_column_index] == user_data[email_column_index]:
            row_index = i + 1  # Add 1 to adjust for 0-based indexing
            break

    user_sheet.update_cell(row_index, metric_column_index, new_value)







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


def update_workout_sheet(current_user, workout_type, duration, workout_sheet):
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
        workout_sheet.append_row(workout_row)
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
    # ui.clear_screen()
    # ui.display_welcome()
    # ui.display_text(INTRO_TEXT, .03)

    try:
        spreadsheet, dataframe = load_google_sheets()
    except Exception as error:
        print(error)
        return

    current_user = None
    while current_user is None:
        try:
            current_user = authenticate_user(dataframe, spreadsheet.get_worksheet(0))
        except Exception as error:
            print(error)
    select_options(current_user, spreadsheet)


main()
