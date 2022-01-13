# Third party imports
import os
import hashlib

# Local application imports
from helper import db

class User():
    def __init__(self):
        self.__username = ''
        self.__password = ''

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        if not username:
            print('Please enter a username.')
        elif db.users.count_documents({"username": username}, limit=1):
            print('That username is already registered')
        else:
            self.__username = username

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plaintext):
        salt = os.urandom(32)
        self._hashed_password = hashlib.pbkdf2_hmac(
            "sha256", plaintext.encode("utf-8"), salt, 100_000
        )