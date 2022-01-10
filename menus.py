from userauth import login, register
from stats import stats_input, stats_daily, stats_weekly


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
        else:
            if option():
                return True

    @staticmethod
    def run(menu):
        user_input = 0
        while(user_input != 9):
            try:
                user_input = int(input())
                boolean = Menu.process(menu, user_input)
                if boolean:
                    return True
                else:
                    return False
            except ValueError:
                print('Please insert a number:')
        print('Goodbye!')

    @staticmethod
    def generate_menu(menu):
        print('=' * 80)
        options = [i for i in dir(menu) if i.startswith('opt_')]
        menu_str = '\n'.join(
            f'{option[-1]}. {getattr(menu, option).__doc__}' for option in options)
        print(menu_str)
        print('=' * 80)
        print('Insert a number: ')


class Main(Menu):
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
        exit()


class Sub(Menu):
    """
    * The class for the sub menu.
    * @staticmethods:
    * opt_1() through to opt_9() -- options for the menu.
    """
    @staticmethod
    def opt_1():
        """Input stats"""
        stats_input()

    @staticmethod
    def opt_2():
        """View daily Support stats"""
        stats_daily()

    @staticmethod
    def opt_3():
        """View weekly Support stat summary"""
        stats_weekly()

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')
        exit()