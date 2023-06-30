def login(df):
    first_name = input("Enter your first name: ").lower()
    last_name = input("Enter your last name: ").lower()
    email = input("Enter your email: ").lower()

    df['Firstname'] = df['Firstname'].str.lower()
    df['Lastname'] = df['Lastname'].str.lower()
    df['Email'] = df['Email'].str.lower()


    matched_users = df[(df['Firstname'] == first_name) & (df['Lastname'] == last_name) & (df['Email'] == email)]

    # Authenticate the user based on the match
    if len(matched_users) > 0:
        print("Authentication successful")
        return email

    else:
        print("Authentication failed")
        return False


def signup(sheet):
    # Prompt the user for sign-up details
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")

    sheet.append_row([first_name, last_name, email])
    print("Sign-up successful")
    return email



