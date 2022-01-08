from userauth import login, register
from stats import *


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
        """Input stats"""
        stats_main()

    @staticmethod
    def opt_2():
        """View daily Support stats"""
        print('Loading...')

    @staticmethod
    def opt_3():
        """View weekly Support stat summary"""
        print('Loading...')

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')
