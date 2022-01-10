# Local application imports
from menus import Menu, Main, Sub
# from menuclasses import MainMenu, SubMenu
from stats import *


def welcome():
    print('doodledy doo doo')


def main():
    welcome()
    Menu.generate_menu(Main)
    loggedin = Menu.run(Main)
    while loggedin:
        Menu.generate_menu(Sub)
        Menu.run(Sub)


if __name__ == '__main__':
    main()
