import time
from helper import db, test_database
from auth import User


def login():
    """
    Checks that the user exists in the database
    Checks that the user's password matches

    Exceptions:
    * LookupError if username isn't found in the database
    * ValueError if the password is incorrect
    """
    print('\nEnter your username and password : ')
    tries = 3
    current_user = User()
    while tries > 0:
        test_database()
        # Ask for a username
        current_user.username = input('Username : ')
        try:
            # Check the database for the username
            user_count = db.users.count_documents(
                {"_User__username": current_user.username})
            if user_count == 0:
                raise LookupError(
                    f'\n** Username: "{current_user.username}" cannot be found in the database. **\n')

            # Ask for a password
            current_user.password = input('\nPassword : ')
            try:
                # Fetch the user's details from the database
                db_user = db.users.find_one(
                    {"_User__username": current_user.username})
                # Check if supplied password matches the password in the database
                if db_user["_hashed_password"] != current_user._hashed_password:
                    raise ValueError(f'\n** The password is incorrect. **\n')

                print(
                    f'\n>> You have successfully logged in as "{current_user.username}".')
                print('>> Taking you to the statistics menu...')
                time.sleep(3)
                # Go to logged in area

            except ValueError as e:
                print(e)
                tries -= 1
                print(f'>> You have {tries} tries left.')

        except LookupError as e:
            print(e)
            tries -= 1
            print(f'>> You have {tries} tries left.')


def register():
    """
    Allows a new user to register for a login
    Checks if the user already exists before saving

    Exceptions:
    * ValueError if the username is blank
    * ValueError if the user already exists in the database
    """
    print('\nLet\'s get you registered!')
    while True:
        test_database()
        new_user = User()
        try:
            # Ask for a username
            new_user.username = input('Enter a username : ')
            # Check if the username is blank/empty
            if not new_user.username:
                raise ValueError(f'\n** Username cannot be blank. **\n')
        except ValueError as e:
            print(e)
        else:
            try:
                # Check the database for the username
                user_count = db.users.count_documents(
                    {"_User__username": new_user.username})
                if user_count:
                    raise ValueError(
                        f'\n** The username "{new_user.username}" is already registered. **\n')

                # Ask for a password and save the user to the database
                new_user.password = input('Enter a password : ')
                db.users.insert_one(new_user.__dict__)
                print(
                    f'\n>> Great! "{new_user.username}" has been registered. You can now login.')
                print('>> Taking you back to the main menu...')
                time.sleep(3)
                # Return to the main menu (run.py)
                break

            except ValueError as e:
                print(e)
