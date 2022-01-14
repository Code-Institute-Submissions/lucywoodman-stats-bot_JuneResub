# Local application imports
from helper import db, test_database
from auth import User


def register():
    print('Let\'s get you registered!')
    while True:
        test_database()
        new_user = User()
        new_user.username = input('Enter a username: ')

        if not new_user.username:
            print('Username cannot be blank.')
            continue

        if db.users.count_documents({"_Login__username": new_user.username}):
            print('That username is already registered.')
            continue

        new_user.password = input('Enter a password: ')
        db.users.insert_one(new_user.__dict__)
        print('You have successfully registered!')
        return True


def login():
    print('Enter your username and password.')
    tries = 3
    while tries > 0:
        test_database()
        current_user = User()
        current_user.username = input('Username: ')

        if not current_user.username:
            print('Username cannot be blank.')
            continue

        if not db.users.count_documents({"_Login__username": current_user.username}):
            tries -= 1
            print('I can\'t find that username.')
            print(f'You have {tries} tries left.')
            continue

        current_user.password = input('Password: ')
        db_user = db.users.find_one(
            {"_Login__username": current_user.username})
        if db_user["_hashed_password"] != current_user._hashed_password:
            tries -= 1
            print('The password is incorrect.')
            print(f'You have {tries} tries left.')
            continue
        else:
            print('-' * 80)
            print('Successful login!')
            return True

    print('Exiting...')
    print('Goodbye!')
