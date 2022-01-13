from auth import Login
from stats import fetch_stats, update_stats


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
            print('Option not found. Try another number:')
        else:
            option()

    @staticmethod
    def run(menu):
        user_input = 0
        while user_input != 9:
            try:
                user_input = int(input())
                Menu.process(menu, user_input)
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
        new_user = Login()
        new_user.handle_user('register')

    @staticmethod
    def opt_2():
        """Register"""
        current_user = Login()
        current_user.handle_user('login')

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')
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
        """View support stat summary"""
        fetch_stats()

    @staticmethod
    def opt_3():
        """Export support stats to JSON"""
        # stats_export()

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')
        exit()
