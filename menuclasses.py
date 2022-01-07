from userauth import login, register


class MainMenu:
    """
    * The class for the main menu.
    * @staticmethods:
    * opt_1() through to opt_9() -- options for the menu.
    """
    @staticmethod
    def opt_1():
        """Login"""
        print('Enter your username and password:')
        if login():
            return True

    @staticmethod
    def opt_2():
        """Register"""
        if register():
            return True

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')


class SubMenu:
    """
    * The class for the sub menu.
    * @staticmethods:
    * opt_1() through to opt_9() -- options for the menu.
    """
    @staticmethod
    def opt_1():
        """Stats"""
        print('Something here...')

    @staticmethod
    def opt_2():
        """Update or whatever"""
        print('Something else here...')

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')
