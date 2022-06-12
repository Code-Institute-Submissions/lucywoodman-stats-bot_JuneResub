import os

# Local application imports
from welcome import welcome
from login import login, register


# def welcome():
#     """
#     * Welcome banner for the program.
#     * Displays ascii robot and title.
#     """
#     ascii_banner = pyfiglet.figlet_format("Stats Bot!!")
#     bot = r"""
#          ___T_
#         | O O |
#         |__u__|
#       (m9\:::/\
#          /___\6
#           |_|
#          (ooo)
#     """
#     print('=' * 80)
#     print('WELCOME TO:')
#     print(ascii_banner + bot)


def main():
    """
    * Main program function where it all begins.
    """
    while True:
        os.system('clear')
        print(welcome('Stats bot'))
        print('\nChoose an option : ')
        print('''
            1 : LOGIN
            2 : REGISTER
            0 : EXIT'''
              )
        choice = input('\nEnter your choice : ')

        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '0':
            print('\nStay awesome!\n')
            exit()
        os.system('clear')


if __name__ == '__main__':
    main()
