class UsernameError(LookupError):
    """ Raised when the username is incorrect """

    def __init__(self, username):
        self.username = username
        self.message = f'\n** Username: "{self.username}" cannot be found in the database. **\n'
        super().__init__(self.message)

    def __str__(self):
        return self.message
