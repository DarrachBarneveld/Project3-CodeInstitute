"""Module runs main app and fetches inputs and google sheets"""
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

# Creating the colorma colours for print statements
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

EXERCISES = [[Y, '1. Running'], [Y, '2. Swimming'],
             [Y, '3. Cycling'], [Y, '4. Weights'],
             [Y, '5. Sports'], [Y, "6. Light"],
             [Y, "7. Other"]]

CHOICE_OPTIONS = [[G, '1. Enter Workout'], [G, '2. View Workouts'],
                  [G, '3. Check BMI'], [G, '4. Dieting Macros Calculator'],
                  [G, '5. Recommended Daily Calories'],
                  [B, '6. Edit Body Metrics'], [R, '7. Logout']]

INTRO_TEXT = [[W, 'Welcome to WorkItOut!\n'], [W, 'Track your workouts!\n'],
              [W, 'Achieve your weight goals!\n'],
              [W, 'Access recommended nutritional information!\n']]

EDIT_DATA = [[Y, '1. Weight'], [Y, '2. Height'], [Y, '3. Age'],
             [Y, '4. Gender'], [Y, '5. Activity Level'], [R, "6. Go Back"]]


def load_google_sheets():
    """
    Load Google Sheets using the gspread library.

    Returns:
        array: Google usersheet, workoutsheet and the pandas user Dataframe.

    Raises:
        gspread.exceptions.APIError: If an error occurs while accessing the
        Google Sheets API.

        gspread.exceptions.SpreadsheetNotFound: If the specified spreadsheet
        is not found.

        gspread.exceptions.WorksheetNotFound: If the default worksheet
        is not found.

        Exception if generalised error
    """
    try:

        creds = Credentials.from_service_account_file('creds.json')
        scoped_creds = creds.with_scopes(GOOGLE_SHEETS_SCOPE)
        gspread_client = gspread.authorize(scoped_creds)

        spreadsheet = gspread_client.open('WorkItOut')
        user_sheet = spreadsheet.get_worksheet(0)
        data = user_sheet.get_all_values()
        dateframe = pd.DataFrame(data[1:], columns=data[0])

        return [spreadsheet, dateframe]

    except APIError as exc:
        raise APIError('An API error occurred. Try again later!') from exc

    except SpreadsheetNotFound as exc:
        raise SpreadsheetNotFound("The spreadsheet was not found!") from exc

    except WorksheetNotFound as exc:
        raise WorksheetNotFound("The worksheet was not found!") from exc

    except Exception as exc:
        raise Exception("Error occurred. Try again later!") from exc


def select_options(current_user, spreadsheet):
    """
    Displays a list of options and prompts the user to select one.
    Selected prompt will run an assosicated function

    Parameters:
        current_user(str): The authenticated user email
        spreadsheet(spreadsheet): The Google SpreadSheet to be updated

    Raises:
        ValueError: If the choice is invalid or not within the choice amount.
    """

    while True:
        print(W + 'What would you like to do?')
        ui.display_text(CHOICE_OPTIONS, .01)
        choice = input("Enter the number corresponding to your choice: ")
        ui.clear_screen()
        user_sheet = spreadsheet.get_worksheet(0)
        work_sheet = spreadsheet.get_worksheet(1)
        try:
            index = int(choice) - 1
            if 0 <= index < len(CHOICE_OPTIONS):
                if index == 0:
                    create_new_workout(current_user, work_sheet)
                elif index == 1:
                    view_all_workouts(current_user, work_sheet)
                    print('\n')
                    ui.back_to_home()
                elif index == 2:
                    prompt_edit_current_metrics(current_user, spreadsheet)
                    user_data = get_current_user_data(current_user, user_sheet)
                    data = fitness_calculator.bmi_calculator(user_data)
                    ui.format_bmi(data)
                elif index == 3:
                    prompt_edit_current_metrics(current_user, spreadsheet)
                    user_data = get_current_user_data(current_user, user_sheet)
                    data = fitness_calculator.dieting_macros(user_data)
                    ui.format_macro_data(data)
                elif index == 4:
                    prompt_edit_current_metrics(current_user, spreadsheet)
                    user_data = get_current_user_data(current_user, user_sheet)
                    data = fitness_calculator.daily_calories(user_data)
                    ui.format_daily_calories(data)
                elif index == 5:
                    edit_current_metrics(current_user, spreadsheet)
                elif index == 6:
                    ui.logout()
                    main()
            else:
                print(R + "\nInvalid choice. Please enter a valid number.")
                print(W)
        except ValueError:
            print(R + "\nInvalid choice. Please enter a valid number.")
            print(W)


def view_all_workouts(current_user, workout_sheet):
    """
    Retrieves workout data from a google sheet and displays to user

    Parameters:
        current_user(str): The authenticated user email
        workout_sheet(sheet): The workout sheet to be updated
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
            table_data.append([
                W + str(workout_type),
                W + str(workout_date),
                W + str(workout_duration)
            ])

        table = tabulate(table_data, table_headers, tablefmt="fancy_grid")
        print(Y)
        print(table)
    # pylint: disable=pylint(broad-exception-caught)
    except Exception as error:
        print("An error occurred:", str(error))


def create_new_workout(current_user, workout_sheet):
    """
    Create a new workout in google sheets document with user inputs and
    authenticated user so workouts are saved with user data

    Args:
        current_user(str): The authenticated user email
        workout_sheet(sheet): The sheet to be updated
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
            if 0 <= int(choice) <= len(EXERCISES):
                workout_type = EXERCISES[index][1]
            else:
                print(R + "\nInvalid choice. Please enter a valid number.")
                print(W)
        except ValueError:
            print(R + "\nInvalid choice. Please enter a valid number.")
            print(W)

    workout_duration = fitness_calculator.validate_input(
        'For how long did you workout in whole minutes? ', 1, 240
        )

    workout_type = workout_type.split('. ')[1]

    update_workout_sheet(
        current_user,
        workout_type,
        workout_duration,
        workout_sheet
    )


def get_current_user_data(current_user, user_sheet):
    """
    Create a new workout in google sheets document with user inputs and
    authenticated user so workouts are saved with user data

    Args:
        current_user(str): The authenticated user email
        user_sheet(sheet): The sheet to be updated

    Returns:
        The user data object
    """

    all_users = user_sheet.get_all_values()
    user_data = [row for row in all_users if row[2] == current_user]
    return user_data[0]


def display_current_metrics(current_user, user_sheet):
    """
    Displays the current user data in the terminal

    Args:
        current_user(str): The authenticated user
        user_sheet(sheet): The sheet that is searched

    """

    user_data = get_current_user_data(current_user, user_sheet)
    ui.format_user_data(user_data)


def prompt_edit_current_metrics(current_user, spreadsheet):
    """
    Displays a prompt for the user to update user data

    Args:
        current_user(str): The authenticated user
        spreadsheet(spreadsheet): The google sheets spreadsheet
    """

    user_sheet = spreadsheet.get_worksheet(0)
    display_current_metrics(current_user, user_sheet)
    print(G)
    ui.type_text('Data will be calculated using your current information', .01)
    print(W)

    choice = fitness_calculator.validate_strings(
        input_string='Do you wish to update information? (Y) or (N):',
        valid=["y", "n"])

    if choice.lower() == 'y':
        edit_current_metrics(current_user, spreadsheet)
        return


def edit_current_metrics(current_user, spreadsheet):
    """
    Edits the current users profile in google sheets

    Args:
        current_user(str): The authenticated user
        spreadsheet(spreadsheet): The google sheets spreadsheet
    """

    user_sheet = spreadsheet.get_worksheet(0)

    display_current_metrics(current_user, user_sheet)
    user_data = get_current_user_data(current_user, user_sheet)

    ui.display_text(EDIT_DATA, .01)
    print(W)

    edit_choice = ''

    while edit_choice == '':
        choice = input("What do you wish to edit? ")
        try:
            index = int(choice) - 1

            if 0 <= index < len(EDIT_DATA):
                edit_choice = EDIT_DATA[index][1].split(' ')[1]
            else:
                ui.display_error(
                    "Invalid choice. Please enter a valid number "
                    )
        except ValueError:
            ui.display_error("Invalid choice. Please enter a valid number.")

    if choice == '6':
        ui.clear_screen()
        select_options(current_user, spreadsheet)
        return

    if edit_choice == 'Activity':
        edit_choice = 'Activity Level'

    update_user_metrics(edit_choice, user_data, user_sheet)


def update_user_metrics(metric, user_data, user_sheet):
    """
    Updates the current metric chosen for the user to and
    updates the user object in the sheet

    Args:
        metric(str): The user object metric to be updated
        user_data(str): The total user_data object to be updated
        user_sheet(sheet): The google sheets user sheet to be updated
    """

    new_value = ''

    if metric == 'Age':
        new_value = fitness_calculator.validate_input(
            'What is your current age? ', 10, 100
            )
    elif metric == 'Weight':
        new_value = fitness_calculator.validate_input(
            'What is your current weight in kg? ',
            40, 160)
    elif metric == 'Height':
        new_value = fitness_calculator.validate_input(
            'What is your current height in cm? ',
            130, 230)
    elif metric == 'Activity Level':
        new_value = fitness_calculator.validate_input(
            'What is your activity level from 1 - 6? ',
            1, 6)
    elif metric == 'Gender':
        new_value = fitness_calculator.validate_strings(
            input_string='Male or Female: ',
            valid=["female", "male"]
            )

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
    ui.clear_screen()


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
    ui.clear_screen()
    ui.display_welcome()
    ui.display_text(INTRO_TEXT, .03)

    try:
        spreadsheet, dataframe = load_google_sheets()
    except Exception as error:
        print(error)
        return

    current_user = None
    while current_user is None:
        try:
            current_user = authenticate_user(dataframe, spreadsheet)
        except Exception as error:
            print(error)

    select_options(current_user, spreadsheet)


main()
