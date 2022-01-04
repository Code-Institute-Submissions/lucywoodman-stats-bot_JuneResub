# Third party imports
import os
import getpass
import hashlib
from xkcdpass import xkcd_password as xp
from pymongo import MongoClient

# Local application imports
if os.path.exists('settings.py'):
    from settings import mongodb_string

# Connect to MongoDB and set the database variables
client = MongoClient(mongodb_string)
db = client.supportStats
users = db.users
stats = db.stats


def menu():
    print('menu')


def welcome():
    print('doodledy doo doo')


def create_password():
    """
    * Creates a randomly generated password using the xkcdpass library.
    * @return(str) gen_password -- the password.
    """
    word_file = xp.locate_wordfile()
    words = xp.generate_wordlist(
        wordfile=word_file, min_length=5, max_length=10)

    gen_password = xp.generate_xkcdpassword(words, numwords=3, delimiter="-")
    return gen_password


def register():
    """
    * Allows new users to register using a chosen username and
    * generated password from create_password().
    * Hashes the password and saves to the connected database.
    """
    username = input('Enter a username: ')
    pwd = create_password()
    print('Please save the password somewhere safe.')
    print(f'Your password is: {pwd}')

    enc_pwd = pwd.encode()
    hash_pwd = hashlib.md5(enc_pwd).hexdigest()

    newUser = {
        "username": username,
        "password": hash_pwd
    }

    db.users.insert_one(newUser)
    print('You have successfully registered!')


def login():
    user = input('Username: ')
    pwd = getpass.getpass()

    enc_pwd = pwd.encode()
    hash_pwd = hashlib.md5(enc_pwd).hexdigest()

    if db.users.count_documents({"username": user}, limit=1):
        result = db.users.find_one({"username": user})

        if result["password"] == hash_pwd:
            print('Successfully logged in!')
            welcome()
        else:
            print('That\'s not the right password, try again.')
    else:
        print('That username isn\'t registered')


login()
