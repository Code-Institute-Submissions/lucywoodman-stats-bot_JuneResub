# Local application imports
from login import register, login
from stats import fetch_stats, update_stats, export_stats


class Menu:
    """
    * A class to power the menus.
    * @staticmethods:
    * process() -- matches the user input with the menu option.
    * run() -- ensures user input is int, runs process().
    * generate_menu() -- creates a str from the menu options and prints it.
    """

    @staticmethod
    def process(menu, user_input):
        option_name = f'opt_{user_input}'
        try:
            option = getattr(menu, option_name)
        except AttributeError:
            print('Option not found.')
            raise ValueError
        else:
            return bool(option())

    @staticmethod
    def run(menu):
        user_input = 0
        while user_input != 9:
            try:
                user_input = int(input())
                return bool(Menu.process(menu, user_input))
            except ValueError:
                print('Please insert a number:')
        print('Goodbye!')

    @staticmethod
    def generate_menu(menu):
        print('=' * 80)
        opts = [i for i in dir(menu) if i.startswith('opt_')]
        menu_str = '\n'.join(
            f'{opt[-1]}. {getattr(menu, opt).__doc__}' for opt in opts)
        print(menu_str)
        print('=' * 80)
        print('Choose an option number: ')


class Main(Menu):
    @staticmethod
    def opt_1():
        """Login"""
        return bool(login())

    @staticmethod
    def opt_2():
        """Register"""
        return bool(register())

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')
        print('Goodbye!')
        exit()


class Sub(Menu):
    """
    * The class for the sub menu.
    * @staticmethods:
    * opt_1() through to opt_9() -- options for the menu.
    """
    @staticmethod
    def opt_1():
        """Add/update stats data"""
        print('Which date do you want to input data for?')
        update_stats()

    @staticmethod
    def opt_2():
        """See support stat data for a day"""
        fetch_stats()

    @staticmethod
    def opt_3():
        """See support stat data for a week"""
        fetch_stats('range')

    @staticmethod
    def opt_4():
        """Export support stat data to JSON"""
        print('Which dates do you want to export data for?')
        export_stats()

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')
        print('Goodbye!')
        exit()
