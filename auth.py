def login(dataframe):
    first_name = input("Enter your first name: ").lower()
    last_name = input("Enter your last name: ").lower()
    email = input("Enter your email: ").lower()

    dataframe['Firstname'] = dataframe['Firstname'].str.lower()
    dataframe['Lastname'] = dataframe['Lastname'].str.lower()
    dataframe['Email'] = dataframe['Email'].str.lower()

    matched_users = dataframe[(dataframe['Firstname'] == first_name) & (dataframe['Lastname'] == last_name) & (dataframe['Email'] == email)]

    # Authenticate the user based on the match
    if len(matched_users) > 0:
        print("Authentication successful")
        return email

    print("Authentication failed")
    return None


def signup(sheet):
    # Prompt the user for sign-up details
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")

    try:
        sheet.append_row([first_name, last_name, email])
        print("Sign-up successful")
        return email
    # pylint: disable=pylint(broad-exception-caught)
    except Exception as exc:
        # pylint: disable=pylint(broad-exception-raised)
        raise Exception("There was an error signing up. Please try again!") from exc


def authenticate_user(dataframe, sheet):
    """
    Prompt the user for a choice of 'login' or 'signup'.

    Args:
        dataframe (object): The google user workout as a pandas dataframe.
        sheet (float): The google user worksheet.

    Returns:
        str: The the current user as an email.
    """

    choice = ''

    while choice not in ["login", "signup"]:
        choice = input("Choose 'login' or 'signup': ").lower()
        if choice not in ["login", "signup"]:
            print("Invalid choice. Please enter 'login' or 'signup'.")

    if choice == 'login':
        return login(dataframe)
    if choice == 'signup':
        return signup(sheet)
    return None
