# Third party imports
import hashlib


class User:
    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def password(self):
        return self._hashed_password

    @password.setter
    def password(self, plaintext):
        self._hashed_password = hashlib.sha256(
            plaintext.encode("utf8")).hexdigest()
