import time
from statbotic.database import data, test_database
from statbotic.user import User
from statbotic.app import app


def login():
    """
    Check that the user exists in the database.
    Check that the user's password matches.

    * @raises(LookupError) -- when username isn't found.
    * @raises(ValueError) -- when password is incorrect.
    """
    print('\nEnter your username and password : \n')
    tries = 3
    current_user = User()
    while tries > 0:
        test_database()
        # Ask for a username
        current_user.username = input('Username : ')
        try:
            # Check the database for the username
            user_count = data.users.count_documents(
                {"_User__username": current_user.username})
            if user_count == 0:
                raise LookupError(
                    f'\n** Username: "{current_user.username}" cannot be found in the database. **\n')

            # Ask for a password
            current_user.password = input('Password : ')
            try:
                # Fetch the user's details from the database
                db_user = data.users.find_one(
                    {"_User__username": current_user.username})
                # Check if supplied password matches the password in the
                # database
                if db_user["_hashed_password"] != current_user._hashed_password:
                    raise ValueError(f'\n** The password is incorrect. **\n')

                print(
                    f'\nYou have successfully logged in as "{current_user.username}".')
                print('Taking you to the statistics menu...')
                time.sleep(2)
                # Go to main app
                app(current_user)

            except ValueError as e:
                print(e)
                tries -= 1
                print(f'** You have {tries} tries left. **')

        except LookupError as e:
            print(e)
            tries -= 1
            print(f'** You have {tries} tries left. **')


def register():
    """
    Allow a new user to register for a login.
    Check if the user already exists before saving.

    * @raises(ValueError) -- when username is blank.
    * @raises(ValueError) -- when user already exists.
    """
    print('\nLet\'s get you registered!\n')
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
                user_count = data.users.count_documents(
                    {"_User__username": new_user.username})
                if user_count:
                    raise ValueError(
                        f'\n** The username "{new_user.username}" is already registered. **\n')

                # Ask for a password and save the user to the database
                new_user.password = input('Enter a password : ')
                data.users.insert_one(new_user.__dict__)
                print(
                    f'\nGreat! "{new_user.username}" has been registered. You can now login.')
                print('Taking you back to the main menu...')
                time.sleep(3)
                # Return to the main menu (run.py)
                break

            except ValueError as e:
                print(e)
