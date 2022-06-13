import traceback
from exceptions import UsernameError
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
                db_user["_hashed_password"] = current_user._hashed_password
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                tries -= 1
                print(f'MESSAGE: {message}')
                print(f'You have {tries} tries left.')

        except UsernameError as error:
            print(error)
            tries -= 1
            print(f'You have {tries} tries left.')
