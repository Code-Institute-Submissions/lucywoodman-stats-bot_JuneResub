class MenuHelper:
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
            option()

    @staticmethod
    def run(menu):
        user_input = 0
        while(user_input != 9):
            try:
                user_input = int(input())
                MenuHelper.process(menu, user_input)
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
