# Third party imports
import hashlib

# Local application imports
from helper import db, test_database

class Login:
    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        if not username:
            print('Please enter a username.')
        else:
            self.__username = username

    @property
    def password(self):
        return self._hashed_password

    @password.setter
    def password(self, plaintext):
        self._hashed_password = hashlib.sha256(plaintext.encode("utf8")).hexdigest()

    def _store_user(self):
        self.username = input('Enter username: ')
        self.password = input('Enter password: ')

    def _check_user(self, option):
        if option == 'register':
            if db.users.count_documents({"_Login__username": self.username}, limit=1):
                print('That username is already registered.')
                return False
        elif option == 'login':
            if not db.users.count_documents({"_Login__username": self.username}, limit=1):
                print('That username isn\'t registered.')
                return False
            if not db.users.count_documents({"_hashed_password": self.password}, limit=1):
                print('The password is wrong.')
                return False
        return True

    def handle_user(self, *option):
        if 'register' in option:
            option = 'register'
            print('Let\'s get you registered!')
            self._store_user()
            test_database()
            proceed = self._check_user(option)
            if proceed:
                db.users.insert_one(self.__dict__)
                print('You are now registered!')
                return True

        if 'login' in option:
            option = 'login'
            print('Enter your username and password.')
            self._store_user()
            test_database()
            proceed = self._check_user(option)
            if proceed:
                print('You\'re now logged in!')
                return True

print('Exiting...')
print('Goodbye!')