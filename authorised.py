from exceptions import PasswordError, UsernameError
from helper import db, test_database
from auth import User


def login():
    print('\nEnter your username and password : ')
    tries = 3
    current_user = User()
    while tries > 0:
        test_database()
        current_user.username = input('Username : ')
        try:
            user_count = db.users.count_documents(
                {"_Login__username": current_user.username})
            if user_count == 0:
                raise UsernameError(current_user.username)

            current_user.password = input('Password : ')
            try:
                db_user = db.users.find_one(
                    {"_Login__username": current_user.username})
                print(db_user["_Login__username"])
                if db_user["_hashed_password"] != current_user._hashed_password:
                    raise PasswordError
            except PasswordError as error:
                print(error)
                tries -= 1
                print(f'You have {tries} tries left.')

        except UsernameError as error:
            print(error)
            tries -= 1
            print(f'You have {tries} tries left.')
