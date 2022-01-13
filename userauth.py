# Third party imports
import getpass
import hashlib
import time
from xkcdpass import xkcd_password as xp


# Local application imports
from helper import db, test_database
from user import User


def register():
    print('Let\'s get you registered!')
    test_database()
    new_user = User()
    new_user.username = input('Enter a username: ')
    new_user.password = input('Enter a password: ')
    db.users.insert_one(new_user.__dict__)
    print('You have successfully registered!')


def login():
    """
    * Captures the user's input username and password,
    * and checks if they exist in the database.
    * If they're already registered, and the input details match, allows login.
    """
    # Set the number of tries the user is allowed.
    attempts = 3
    # Create a login loop while the attempts are greater than 0.
    while attempts > 0:
        # Capture the user input for the username.
        user = input('Username: ')
        test_database()

        # Check if the username exists in the database.
        if not users.count_documents({"username": user}, limit=1):
            # If the username doesn't match any in the db,
            # then reduce attempts by 1.
            attempts -= 1
            print(f'I can\'t find that user. You have {attempts} tries left.')
            print('-' * 80)
            continue

        # Capture the user input for the password.
        pwd = getpass.getpass()

        # Encode and hash the password to match how the db stores passwords.
        enc_pwd = pwd.encode()
        hash_pwd = hashlib.md5(enc_pwd).hexdigest()
        # Fetch the user's info from the database.
        result = users.find_one({"username": user})

        # If the hashed password matches the hashed password in the db,
        # let the user login.
        if result["password"] != hash_pwd:
            # If the hashed password doesn't match, then reduce attempts by 1.
            attempts -= 1
            print(
                f'The password is incorrect. You have {attempts} tries left.')
            print('-' * 80)
            continue
        else:
            print('-' * 80)
            print('You have successfully logged in!')
            return True

    print('Exiting...')
    print('Goodbye!')
