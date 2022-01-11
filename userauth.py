# Third party imports
import getpass
import hashlib
from xkcdpass import xkcd_password as xp
import time

# Local application imports
from helper import test_database, users


def create_password():
    """
    * Creates a randomly generated password using the xkcdpass library.
    * @return(str) gen_password -- the password.
    """
    word_file = xp.locate_wordfile()
    # Choose words between 5 and 10 characters long.
    words = xp.generate_wordlist(
        wordfile=word_file, min_length=5, max_length=10)

    # Create a random password made up of 3 words separated with a hyphen.
    gen_password = xp.generate_xkcdpassword(words, numwords=3, delimiter="-")
    return gen_password


def register():
    """
    * Allows new users to register using a chosen username and
    * generated password from create_password().
    * Hashes the password and saves to the connected database.
    """
    # Create a register while loop.
    while True:
        # Ask for a username from the user.
        username = input('Enter a username: ')

        # Check if the username already exists in the db.
        # If it does, tell the user and go back to beginning of the loop.
        if users.count_documents({"username": username}, limit=1):
            print('That username is already registered. Try another.')
            continue
        # If the username doesn't exist in the db, generate a password.
        # Then display the password and let them login.
        else:
            print('Generating password...')
            time.sleep(1)
            pwd = create_password()
            print('-' * 80)
            print(f'Your password is: {pwd}')
            print('Please save the password somewhere safe.')

            enc_pwd = pwd.encode()
            hash_pwd = hashlib.md5(enc_pwd).hexdigest()

            newUser = {
                "username": username,
                "password": hash_pwd
            }

            users.insert_one(newUser)
            print('-' * 80)
            print('You have successfully registered!')
            print('Go ahead and login:')
            login()
        return


def login():
    """
    * Captures the user's input username and password, and checks if they exist in the database. 
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
            # If the username doesn't match any in the db, then reduce attempts by 1.
            attempts -= 1
            print(
                f'That username isn\'t registered. You have {attempts} tries left.')
            print('-' * 80)
            continue

        # Capture the user input for the password.
        pwd = getpass.getpass()

        # Encode and hash the password to match how the database stores passwords.
        enc_pwd = pwd.encode()
        hash_pwd = hashlib.md5(enc_pwd).hexdigest()
        # Fetch the user's info from the database.
        result = users.find_one({"username": user})

        # If the hashed password matches the hashed password in the db, let the user login.
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
